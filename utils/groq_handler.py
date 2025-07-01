import os
import requests
from config.settings import GROQ_API_KEY, GROQ_API_URL, DEFAULT_MODEL, DEFAULT_TEMPERATURE

def call_groq_model(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": DEFAULT_TEMPERATURE
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

<<<<<<< HEAD
    if response.status_code != 200:
        raise Exception(f"Groq API failed: {response.status_code} - {response.text}")

    try:
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as e:
        raise Exception(f"Groq response parsing failed: {e}")
=======
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    streaming=True
)

def call_groq_model(system_prompt, query_prompt):
    """Non-streaming fallback version."""
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query_prompt)
    ]
    response = llm.invoke(messages)
    return response.content.strip()

def stream_groq_response(system_prompt, query_prompt):
    """Streaming version for real-time UI."""
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query_prompt)
    ]
    for chunk in llm.stream(messages):
        if hasattr(chunk, "content"):
            yield chunk.content

def generate_groq_response(prompt, system_prompt="You are a helpful data analyst."):
    return call_groq_model(system_prompt, prompt)
>>>>>>> e1bab98 (Modified the code)
