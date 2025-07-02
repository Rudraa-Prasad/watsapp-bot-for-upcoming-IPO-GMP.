from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from twilio.rest import Client
from dotenv import load_dotenv  # to read K:V from .env file
import uvicorn
import os

load_dotenv()
GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
genai.configure(api_key=GOOGLE_GENAI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# Simple in-memory store to track if a user is sending the first message or a follow-up
user_state = {}


@app.get("/")
async def root():
    return {"message": "Welcome to the WhatsApp Bot API"}


@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    print(form_data)
    
    user_query = form_data.get('Body', "japanah")
    from_number = form_data.get('From')
    print(user_state)

    # Check if user exists in the state tracking
    if from_number not in user_state:
        # If first message, respond with a greeting
        user_state[from_number] = "interacted"
        response_text = (
            "Hey There whatsupppppp!!!!!!!!\n\n"
            "Hi, I am RudraChat, your personal assistant here to answer any questions related to IPO and stock market."
            "How may I assist you today? *created by Rudra Prasad*"
        )
    elif user_query.strip().lower() in ("hello", "hi", "hey"):
        response_text = "Hey, RudraChat here, here to answer any questions related to IPO and stock market.. How may I help you?"
    else:
        # Subsequent queries, process with LLM
        prompt_text = f"""
        You are a personal assistant bot designed to answer questions related to upcoming IPOs in Indian stock market. Your role is to provide accurate, concise, and correct responses about :
        Grey market price of that IPO. 
        positive points for investing.
        negative points to consider.

        If user asks anything outside this context, politely respond, 'Sorry i am unable to answer this question as i can only respond to queries related to Stock market, IPOs.' 
        If the user asks about you, say you are RudraChat. If they say thanks, goodbye, or send an emoji, reply accordingly. 
        Ensure to include a line break and end each response with '*RudraChat*'. 

        User Query: {user_query}
        """

        response = model.generate_content(prompt_text)
        response_text = response.text

    # Send response back to the user via WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(response_text)
    print(twilio_response)
    
    return Response(content=str(twilio_response), media_type="application/xml")



# Add this block to run the server locally
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
