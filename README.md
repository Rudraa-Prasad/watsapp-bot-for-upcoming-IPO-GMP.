## RudraChat - WhatsApp Bot for IPO & Stock Market Queries

**RudraChat** is a WhatsApp chatbot designed to help users with queries related to **upcoming IPOs in the Indian stock market**. Built with **FastAPI**, **Twilio**, and **Google Gemini 1.5 Flash**, it provides insights like grey market prices, positive and negative aspects of IPOs, and general stock market information.

---

## ✨ Features

* Conversational responses powered by **Google Generative AI (Gemini)**
* WhatsApp integration via **Twilio API**
* Lightweight backend built with **FastAPI**
* Basic session memory to differentiate new and returning users

---

## ⚙️ Tech Stack

* Python 3
* FastAPI
* Twilio API (WhatsApp Messaging)
* Google Generative AI (Gemini 1.5 Flash)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Rudraa-Prasad/whatsapp-bot-for-upcoming-IPO-GMP.git
cd whatsapp-bot-for-upcoming-IPO-GMP
```

### 2. (Optional) Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file in the root folder:

```env
GOOGLE_GENAI_API_KEY=your_google_genai_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

### 5. Start the FastAPI server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔗 Twilio Webhook Configuration

1. Go to the [Twilio Console](https://www.twilio.com/console).
2. Navigate to **Messaging → WhatsApp Sandbox Settings**.
3. Set the **Webhook URL** to:

---


## 👨‍💻 Author

Developed by **Rudra Prasad**
AI/LLM Engineer

[LinkedIn](https://linkedin.com/in/rudra-prasad-684239159) | [Email](pdrudra.121@gmail.com)

---
