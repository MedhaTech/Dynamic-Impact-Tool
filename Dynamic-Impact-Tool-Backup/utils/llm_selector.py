import os
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI

def get_llm(model_source="groq"):
    if model_source == "groq":
        return ChatOpenAI(
            temperature=0.3,
            model="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
    elif model_source == "ollama":
        return Ollama(model="gemma:7b", base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    else:
        raise ValueError("Invalid model source")
