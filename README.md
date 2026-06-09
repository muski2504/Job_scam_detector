# 🛡️ ScamShield — Intelligent Job Fraud Detection System

Protecting Indian job seekers from fraudulent job postings using NLP and Machine Learning.

## Tech Stack
Python · DistilBERT · HuggingFace · Flask · Streamlit

## Dataset
- 1150 labeled job posts from 9 platforms
- Sources: LinkedIn, Naukri, Reddit, Internshala, WhatsApp, Telegram

## How It Works
1. Paste any job post
2. Rule-based checker scans for red flags
3. DistilBERT model predicts scam probability  
4. Trust score 0-10 with reasons displayed

## Run Locally
```bash
pip install -r requirements.txt
python api.py
streamlit run app.py
```