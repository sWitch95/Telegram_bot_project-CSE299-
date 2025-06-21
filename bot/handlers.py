from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from rag.langchain_pipeline import answer_query  # ✅ LangChain query function import

TOKEN = '7677389671:AAE_ILH0WyacSU21vqUlLCIn_m-gSY-pNfg'
BOT_USERNAME: Final = '@medication_remider_and_info_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your medication assistant bot. Ask me about any medicine.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can ask me things like:\n- What is Napa?\n- What are the side effects of Seclo?")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command response!")

# 💬 Response logic
def handle_response(text: str) -> str:
    processed = text.lower()

    if any(kw in processed for kw in ["what is", "use of", "side effect", "why", "how to use", "dosage"]):
        return answer_query(processed)

    elif "reminder" in processed:
        return "I can help you set a reminder for your medication. (Reminder feature coming soon!)"
    
    elif "hello" in processed or "hi" in processed:
        return "Hi! I'm here to help with medicine-related questions."

    else:
        return "I'm not sure about that. Please ask me about a medication."

# 🔄 Handles every user message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group' and BOT_USERNAME in text:
        new_text = text.replace(BOT_USERNAME, '').strip()
        response = handle_response(new_text)
    elif message_type == 'private':
        response = handle_response(text)
    else:
        return  # Ignore non-mention group messages

    print('Bot:', response)
    await update.message.reply_text(response)

# 🛠️ Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update "{update}" caused error "{context.error}"')

# 🚀 Run bot
if __name__ == '__main__':
    print("🤖 Starting the bot...")
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('custom', custom_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    print("✅ Bot is running...")
    application.run_polling(poll_interval=3)
