from .groq_handler import call_groq_model
from .ollama_handler import call_ollama_model

def get_llm(model_source="groq"):
    if model_source == "groq":
        return lambda prompt: call_groq_model("You are a helpful assistant.", prompt)
    else:
        return lambda prompt: call_ollama_model("You are a helpful assistant.", prompt)

