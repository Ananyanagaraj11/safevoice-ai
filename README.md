# SafeVoice AI 🔊🛡️  
Detect emotional and verbal abuse for women's safety using AI & NLP

Live Demo : (https://safevoiceai.netlify.app/) |
GitHub Repo : https://github.com/Ananyanagaraj11/safevoice-ai

---

## About SafeVoice

**SafeVoice AI** is a web-based application designed to help promote **women’s safety and mental well-being**. It captures and analyzes voice conversations to detect signs of **emotional distress**, **verbal abuse**, and **toxic behavior** using artificial intelligence.

The system uses **Whisper** for speech-to-text and a transformer-based NLP model to extract **emotions** and **abuse patterns** — all processed **locally** with full respect for user privacy.

---

## Why SafeVoice Matters!!

Many women face **invisible abuse**—emotional or verbal—that goes unreported. SafeVoice AI enables users to:

- Detect **toxic, manipulative, or threatening** language  
- Recognize emotions like **fear, sadness, and anger**
- Document abuse via **automated PDF reports**
- Seek help with **emergency contact and email support suggestions**

---

## Features

- 🎙️ Record or Upload voice clips (MP3/WAV)
- 🔁 Transcription with **OpenAI Whisper**
- ⚠️ Abuse detection and **emotion classification**
- 📊 View analysis via **charts** and **emotion tables**
- 📝 Export **PDF safety reports**
- 📱 Optimized for web and mobile with **React**
- 🔒 All analysis runs locally — no data uploaded

---

## 🛠️ Tech Stack

- **React (Frontend UI)**
- **Python (Flask API Backend)**
- **Whisper** – Speech-to-text
- **Hugging Face Transformers** – NLP abuse/emotion detection
- **ReportLab** – PDF generation
- **Chart.js / HTML Canvas** – Emotion visualizations

---

## Getting Started

### 1. Clone the repository
git clone https://github.com/Ananyanagaraj11/safevoice-ai.git
cd safevoice-ai 

### 2. Install dependencies
Backend (Python):
pip install -r requirements.txt

Frontend (React): [it is in Safevoice-ai folder]
npm install

### 3. Start the app
Start backend server:
python app.py

Start frontend (React):
npm start
