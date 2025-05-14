import logging
import spacy
from core.intent import get_response
from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.getenv("NEWS_API_KEY")



# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.ERROR)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def chat():
    print("LetsChat is running! (Type 'bye' to exit)")
    waiting_for_name = False
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower():
            response, _ = get_response(user_input)
            print("LetsChat:", response)
            break
        response, waiting_for_name = get_response(user_input, waiting_for_name)
        print("LetsChat:", response)

if __name__ == "__main__":
    chat()
