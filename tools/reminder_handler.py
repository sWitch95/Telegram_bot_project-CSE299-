import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
import re

# Dictionary to keep scheduled jobs
scheduled_reminders = {}

# ✅ Parse time string (like "7:30 PM")
def parse_time_string(time_str: str) -> datetime:
    try:
        now = datetime.now()
        parsed_time = datetime.strptime(time_str.strip(), "%I:%M%p")
        scheduled_time = now.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0)
        if scheduled_time < now:
            scheduled_time += timedelta(days=1)
        return scheduled_time
    except Exception as e:
        print(f"❌ Time parsing failed: {e}")
        return None

# 🔔 Reminder job
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    medicine = job_data["medicine"]
    repeat = job_data.get("repeat", False)

    print(f"🔔 Sending reminder to {chat_id}: {medicine}")
    await context.bot.send_message(chat_id=chat_id, text=f"⏰ ওষুধ মনে করিয়ে দিচ্ছি:\n💊 {medicine}")

    # Re-schedule for tomorrow if it's a daily reminder
    if repeat:
        next_time = datetime.now() + timedelta(days=1)
        run_time = next_time.replace(hour=job_data['hour'], minute=job_data['minute'], second=0, microsecond=0)
        context.job_queue.run_once(
            send_reminder,
            when=(run_time - datetime.now()).total_seconds(),
            data=job_data,
            name=f"reminder_{chat_id}_{medicine}_{run_time.strftime('%H%M')}"
        )

# ✅ /remind command
async def add_reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Join args into full message
        full_command = ' '.join(context.args)
        match = re.match(r"(.*) at (\d{1,2}:\d{2}\s*[apAP][mM])(?:\s+everyday)?", full_command)

        if not match:
            await update.message.reply_text(
                "⚠️ ভুল ফরম্যাট। সঠিকভাবে দিন:\n/remind Napa at 9:00pm\n/remind Seclo at 7:30am everyday"
            )
            return

        medicine = match.group(1).strip()
        time_str = match.group(2).replace(" ", "").upper()
        repeat = 'everyday' in full_command.lower()

        reminder_time = parse_time_string(time_str)
        if not reminder_time:
            await update.message.reply_text("⚠️ সময় সঠিক ফরম্যাটে দিন (যেমন: 9:00pm)")
            return

        delay = (reminder_time - datetime.now()).total_seconds()

        job_data = {
            "chat_id": update.message.chat_id,
            "medicine": medicine,
            "repeat": repeat,
            "hour": reminder_time.hour,
            "minute": reminder_time.minute
        }

        job_name = f"reminder_{update.message.chat_id}_{medicine}_{reminder_time.strftime('%H%M')}"
        context.job_queue.run_once(send_reminder, when=delay, data=job_data, name=job_name)

        # Store reminder
        scheduled_reminders[job_name] = {
            "user": update.message.chat_id,
            "medicine": medicine,
            "time": reminder_time.strftime("%I:%M %p"),
            "repeat": repeat
        }

        await update.message.reply_text(
            f"✅ মনে করিয়ে দেয়া হবে: {medicine} @ {reminder_time.strftime('%I:%M %p')}" +
            (" প্রতিদিন।" if repeat else "")
        )

    except Exception as e:
        print(f"❌ Reminder setup failed: {e}")
        await update.message.reply_text("⚠️ মনে করানোর সময় সেট করতে ব্যর্থ। ফরম্যাট ঠিক আছে কিনা দেখুন।")

# 📋 List reminders
async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_reminders = [r for r in scheduled_reminders.values() if r["user"] == chat_id]

    if not user_reminders:
        await update.message.reply_text("ℹ️ আপনার কোনো রিমাইন্ডার নেই।")
        return

    msg = "📋 আপনার রিমাইন্ডার তালিকা:\n"
    for i, r in enumerate(user_reminders, 1):
        repeat_text = " (প্রতিদিন)" if r['repeat'] else ""
        msg += f"{i}. {r['medicine']} @ {r['time']}{repeat_text}\n"

    await update.message.reply_text(msg)

# 🧹 Cancel all
async def cancel_all_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    canceled = 0
    for job in context.job_queue.jobs():
        if job.data and job.data.get("chat_id") == chat_id:
            job.schedule_removal()
            canceled += 1

    await update.message.reply_text(f"🧹 {canceled} টি রিমাইন্ডার বাতিল করা হয়েছে।")
