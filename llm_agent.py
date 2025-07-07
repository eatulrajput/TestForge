# llm_agent.py

from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Set your Groq API key here (or use environment variables)
api_key =os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Groq_API_Key is not set in the environment or .env file")

client = Groq(api_key=api_key)

# MODEL = "mixtral-8x7b-32768"  # or try: llama3-70b-8192, gemma-7b-it
MODEL = "llama3-70b-8192"

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes and refines unit tests in C++ using Google Test."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
