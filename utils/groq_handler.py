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

from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def query_groq(prompt):
    if len(prompt) > 8000:
        prompt = prompt[:8000]

    response = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=[
            {"role": "system", "content": "You are a senior data scientist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()
