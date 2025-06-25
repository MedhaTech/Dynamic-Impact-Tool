import ollama
import os
import requests
from langchain_community.llms import Ollama

def call_ollama_model(system_prompt, query_prompt):
    prompt = f"{system_prompt}\n\n{query_prompt}"
    model = Ollama(model="gemma:2b")
    return model.invoke(prompt)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def call_groq_model(system_prompt, user_prompt):
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Groq API Error {response.status_code}: {response.text}")
