from utils.groq_handler import call_openai_model, call_ollama_model
from dotenv import load_dotenv

load_dotenv()
# utils/llm_selector.py

def get_llm(model_source="openai"):
    if model_source in ["openai", "groq"]:  
        def llm(prompt):
            system_prompt = "You are a helpful data analyst. Provide clear and concise responses."
            return call_openai_model(system_prompt, prompt)
        return llm

    elif model_source == "ollama":
        def llm(prompt):
            return call_ollama_model(prompt)
        return llm

    else:
        raise ValueError(f"Unsupported model source: {model_source}")
