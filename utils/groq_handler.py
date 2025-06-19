import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# def query_groq(prompt):
#     from openai import OpenAI
#     import os

#     client = OpenAI(
#         api_key=os.getenv("GROQ_API_KEY"),
#         base_url="https://api.groq.com/openai/v1"
#     )

#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": "You are a senior data scientist."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.5,
#         max_tokens=1024,
#     )
#     return response.choices[0].message.content.strip()
# utils/groq_handler.py

# utils/groq_handler.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq_model(system_prompt, user_prompt):
    if not GROQ_API_KEY:
        return "GROQ_API_KEY not found. Please check your .env file."

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 1000
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"LLM failed: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception while querying LLM: {e}"
