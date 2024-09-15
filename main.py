from fastapi import FastAPI, Request, Form
#import twilio
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from twilio.rest import Client
from dotenv import load_dotenv  # to read K:V from .env file


import os

GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
model = genai.GenerativeModel("gemini-1.5-flash")

load_dotenv()
app = FastAPI()

# Simple in-memory store to track if a user is sending the first message or a follow-up
user_state = {}


@app.get("/")
async def root():
    return {"message": "Welcome to the WhatsApp Bot API"}

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    user_query = form_data.get('Body')
    from_number = form_data.get('From')

    # Check if user exists in the state tracking
    if from_number not in user_state:
        # If first message, respond with "How may I help you?"
        user_state[from_number] = "interacted"  # Mark this user as already interacted
        response_text = "Hi. I am NIVESH. A banker buddy to you. How may I help you today?"
    elif user_query.strip().lower() == "hello" or "Hi" or "hi":
        response_text = "Hey, How may I help you?"
    else:
        # Subsequent queries, process with LLM
        prompt_text = f"generate result for user query in less than 150 words: {user_query}"
        response = model.generate_content(prompt_text)
        response_text = response.text

    # Send response back to the user via WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(response_text)
    return str(twilio_response)
