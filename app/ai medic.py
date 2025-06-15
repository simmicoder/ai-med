import cohere
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
api_key = os.getenv("COHERE_API_KEY")  # Get key from .env

if not api_key:
    raise ValueError("COHERE_API_KEY is missing from .env file!")

co = cohere.Client(api_key)

def ask_for_otc_meds(symptoms):
    response = co.chat(
        message=f"Suggest over-the-counter medication for: {symptoms}. Format response as advice, medication name, and dosage.",
        model="command-r",
        temperature=0.7,
    )
    text = response.text.strip().split("\n")

    return {
        "advice": text[0],
        "medication": text[1] if len(text) > 1 else "N/A",
        "dosage": text[2] if len(text) > 2 else "N/A",
    }