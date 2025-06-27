# chains/llms.py

from langchain.chat_models import ChatOpenAI
from config.settings import GROQ_API_KEY

class GroqChatLLM(ChatOpenAI):
    def __init__(self, model="llama3-8b-8192", temperature=0.3):
        super().__init__(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature
        )
