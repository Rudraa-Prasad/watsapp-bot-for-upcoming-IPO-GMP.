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
    user_query = "japanah"
    user_query = form_data.get('Body')
    print(user_query)
    from_number = form_data.get('From')
    print(user_state)
    # Check if user exists in the state tracking
    if from_number not in user_state:
        # If first message, respond with "How may I help you?"
        user_state[from_number] = "interacted"  # Mark this user as already interacted
        response_text = "Hi. I am RudraChat. An assistant for all your needs. How may I help you today? *created by Rudra Prasad*"
    elif user_query.strip().lower() in ("hello", "hi", "hey"):
        response_text = "Hey, RudraChat here, How may I help you?"
    else:
        # Subsequent queries, process with LLM
        prompt_text = f"""Generate a concise response for the user's query. 
For simple questions, keep the answer under 100 words. For more complex queries, 
you can extend the response up to 170 words. Always use clear and easy-to-understand
language, so that anyone can grasp the information. Ensure to include a line break and
end each response with '*RudraChat*'. {user_query}"""



        response = model.generate_content(prompt_text)
        response_text = response.text

    # Send response back to the user via WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(response_text)
    print(twilio_response)
    #return twilio_response
    return Response(content=str(twilio_response), media_type="application/xml")


# Add this block to run the server locally
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)