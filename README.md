# 🩺 Medication Reminder and Info Bot

This project presents a **Telegram-based AI Medicine Assistant** that supports both **Bangla 🇧🇩** and **English 🇬🇧**.  
The system is designed to answer **medicine-related queries**, process **medicine images** via OCR, handle **voice-based queries**, and manage **medicine reminders**.  
It combines **Natural Language Processing (NLP)**, **Retrieval-Augmented Generation (RAG)**, and **speech technologies** to create a robust and user-friendly assistant.

---
## 📌 Project Overview

- **Project Title**: Medication Reminder and Info Bot  
- **Course**: CSE 299 – Junior Design Project (Summer 2025)  
- **Section**: 03  
- **Supervisor**: Dr. Shafin Rahman  
- **Group Number**: 2  

**Team Members**:
- Aqib Ahmed  
- Towhidul Islam  
- Md. Yousuf   
- M.G. Rabbi Hossen  

---


## 🚀 Key Features

- **Bilingual Support**: Seamless interaction in both **Bangla** and **English**.  
- **Voice Interaction**: Users can send queries as **voice messages**, and the bot responds in the same language.  
- **Image-based Recognition**: Supports **OCR (Tesseract)** for extracting medicine names and details from uploaded images.  
- **Intelligent Retrieval (RAG)**: Uses **LangChain + FAISS + SentenceTransformer embeddings** to deliver accurate, context-aware responses.  
- **Medicine Reminders**: Users can set, list, and cancel reminders for their medicines.  
- **Groq LLM Integration**: Powered by **Groq Llama-3.1-8B** for fast, reliable inference.  

---

## 🏗️ System Architecture

The architecture integrates multiple components into a single pipeline:

1. **Telegram Bot Interface** – Acts as the primary frontend for user interaction.  
2. **Document & Image Processing** – Extracts text using PyPDF, DOCX readers, and OCR for medicine photos.  
3. **Vector Database (FAISS)** – Stores and retrieves embeddings for efficient query matching.  
4. **RAG Pipeline** – Embeds queries, performs similarity search, and forwards context to the LLM.  
5. **Voice Processing Module** – Speech-to-Text (STT) and Text-to-Speech (TTS) ensure natural user interaction.  
6. **Reminder System** – Manages medicine reminders with notifications inside Telegram.  

---

## 📊 Evaluation

The system was evaluated using **1000 natural queries** (500 Bangla + 500 English).  
Performance was measured using **BERTScore** to compute **Accuracy, Precision, Recall, and F1-score**.

| Language | Queries | Accuracy (%) | Precision | Recall | F1 Score |
|----------|---------|--------------|-----------|--------|----------|
| Bangla   | 500     | 69.8         | 0.70      | 0.69   | 0.695    |
| English  | 500     | 71.2         | 0.72      | 0.71   | 0.715    |
| Overall  | 1000    | 70.4         | 0.71      | 0.70   | 0.705    |

These results demonstrate that the bot achieves **over 70% accuracy** across both languages, with balanced precision, recall, and F1-score.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/medicine-assistant-bot.git
cd medicine-assistant-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:

```
TOKEN=your_telegram_bot_token
BOT_USERNAME=your_bot_username
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the Bot
```bash
python -m bot.handlers
```

---

## 📦 Tech Stack

- **Frontend**: Telegram Bot API  
- **OCR**: Tesseract + OpenCV  
- **Vector Store**: FAISS  
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)  
- **LLM**: Groq Llama-3.1-8B-Instant  
- **Voice Processing**: Google Speech Recognition, gTTS, pyttsx3  
- **Frameworks**: LangChain, Python-Telegram-Bot  

---

## 🔮 Future Work

This system can be extended in the following directions:

- Improve OCR performance on **low-quality images** captured from mobile devices.  
- Integrate **multimodal embeddings** (image + text) for better retrieval.  
- Deploy as a **scalable cloud service** with Docker and Kubernetes.  
- Extend reminder system to support **recurring schedules** and push notifications.  
- Build a **mobile app frontend** to complement the Telegram interface.  

---

## 📄 License & Acknowledgements

This project is created for educational purposes under the supervision of **Dr. Shafin Rahman**.  
All third-party models and datasets are used in accordance with their respective licenses.
