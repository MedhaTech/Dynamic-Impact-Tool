from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from config.settings import GROQ_API_KEY
import os

# Monkeypatch for LangChain to use Groq (via OpenAI-compatible endpoint)
from langchain_community.chat_models import ChatOpenAI

class GroqChatLLM(ChatOpenAI):
    def __init__(self, model="llama3-8b-8192", temperature=0.3, **kwargs):
        super().__init__(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )

def generate_summary(columns, sample_rows):
    prompt = ChatPromptTemplate.from_template(
        """You are an expert data analyst.

Given a dataset with the following columns:
{columns}

And sample data rows:
{rows}

Generate a concise summary covering:
- What this dataset might be about
- Who might use it
- Key variables and meaning
- Any patterns you notice
"""
    )

    formatted_prompt = prompt.format_messages(
        columns=", ".join(columns),
        rows=sample_rows[:5]
    )

    llm = GroqChatLLM()
    response = llm(formatted_prompt)

    return response.content.strip()
