# 🏥Medication Reminder and Info Bot

A comprehensive Telegram bot that provides medicine information in both English and Bengali, featuring RAG (Retrieval-Augmented Generation) capabilities, OCR text recognition, voice interaction, and medication reminders.

## ✨ Features

### 🌐 Bilingual Support
- **English & Bengali**: Ask questions in either language and get responses in your preferred language
- **Auto-detection**: Automatically detects the language of your query
- **Smart Translation**: Uses Google Translator for seamless language conversion

### 🤖 RAG-Powered Medicine Information
- **FAISS Vector Database**: Fast similarity search across medicine dataset
- **LLM Integration**: Uses Groq's Llama-3.1-8b-instant model for intelligent responses
- **Comprehensive Dataset**: Includes generic medicines, brand names, and detailed information

### 📸 OCR Text Recognition
- **Medicine Package Reading**: Upload photos of medicine packages or prescriptions
- **Dual Language OCR**: Supports both English and Bengali text recognition
- **Interactive Query Selection**: Choose specific information types after OCR

### 🎤 Voice Interaction
- **Speech-to-Text**: Send voice messages in Bengali or English
- **Text-to-Speech**: Get voice responses in the detected language
- **Multi-format Support**: Handles OGG to WAV conversion automatically

### ⏰ Medication Reminders
- **Time-based Reminders**: Set reminders like `/remind Paracetamol at 9:00pm`
- **Daily Repeating**: Add `everyday` for daily medication schedules
- **Reminder Management**: List and cancel reminders as needed

## 🛠️ Technology Stack

### Backend & AI
- **Python 3.8+**
- **LangChain**: RAG pipeline and document processing
- **FAISS**: Vector similarity search
- **Groq API**: LLM for intelligent responses
- **SentenceTransformers**: Text embeddings (all-MiniLM-L6-v2)

### Telegram Bot
- **python-telegram-bot**: Telegram Bot API wrapper
- **Async/Await**: Modern Python async programming

### Voice Processing
- **SpeechRecognition**: Google Speech Recognition API
- **gTTS**: Google Text-to-Speech for Bengali
- **pyttsx3**: Local TTS engine for English
- **PyDub**: Audio format conversion

### Image Processing
- **Tesseract OCR**: Text extraction from images
- **OpenCV**: Image preprocessing
- **PIL**: Image handling

### Translation
- **deep-translator**: Google Translate integration
- **langdetect**: Language detection

## 📁 Project Structure
