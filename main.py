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
        response_text = "" Wishing *MEGHA* a beautiful Valentine's Day filled with smiles, warmth, and special moments!

Hi, I am RudraChat, your personal assistant here to answer any questions you may have about Rudra Prasad. How may I assist you today? *created by Rudra Prasad*"
    elif user_query.strip().lower() in ("hello", "hi", "hey"):
        response_text = "Hey, RudraChat here, How may I help you?"
    else:
        # Subsequent queries, process with LLM
#         prompt_text = f"""you are helpful assistant 'RudraChat'. Generate a concise response for the user's query. 
# For simple questions, keep the answer under 100 words. For more complex queries, 
# you can extend the response up to 200 words. Always use clear and easy-to-understand
# language, so that anyone can grasp the information. and if the user_query is like 'write poem' 
# or anything you need to do that also. if user ask anything about you , say I am RudraChat, a personal assistant designed to share information about Rudra Prasad. I can answer your questions about his background, hobbies, values, goals, and what he is looking for in a life partner. if user thanks or say good bye or send emoji reply accordingly. Ensure to include a line break and
# end each response with '*RudraChat*'. {user_query}"""
        
                prompt_text = f"""
                You are a personal assistant bot designed to answer questions from Rudra Prasad's potential wife. Your role is to provide accurate, concise, and positive responses about Rudra based on the following details:

Personal Information:

Name: Rudra Prasad
Date of Birth: 14th April 1993
Place of Birth: Ramgarh, Jharkhand
Height: 5 feet 6 inches
Gotra: Kashyap
Religion/Caste: Hindu/Shoundik
Education:

Masters: IIT Madras (Graduated in 2023)
Bachelors: C. V. Raman College of Engineering, Bhubaneswar 
Work Experience:

Current Role: Tech Lead (AI) at HCLTech
Previous Role: Assistant Manager at Jindal Steel (2 years)
Hobbies and Interests:

Loves investing and learning about the stock market
Politically aware and values staying informed
 women empowerment and mutual respect for both families
Values and Future Goals:

Believes in mutual respect and equality in marriage
Prioritizes family values and harmony between both families
Aims to continue growing in his career and making a meaningful impact
Looks forward to supporting his wife's aspirations and building a respectful partnership
Expectations from a Life Partner:

Someone who shares values of mutual respect and understanding
A partner who values family and personal growth
Someone with a positive outlook, empathy, and a willingness to work as a team in life
If she asks anything outside this context, politely respond, 'I know only about Rudra.' Always ensure responses are optimistic and present Rudra in a positive light.
                if user ask anything about you , say you are RudraChat. if user thanks or say good bye or send emoji reply accordingly. Ensure to include a line break and
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
