from config.settings import GROQ_API_KEY
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class GroqChatLLM(ChatOpenAI):
    def __init__(self, model="llama3-8b-8192", temperature=0.3, **kwargs):
        super().__init__(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )

def generate_insight_categories(columns, rows):
    prompt = ChatPromptTemplate.from_template(
        """You are a senior AI data scientist.

Based on the following columns:
{columns}

And sample rows:
{rows}

Suggest 5–7 useful **insight categories** people might want to analyze. Return only a **Python list of strings** like:

["Performance Trends", "Demographic Variance", "Learning Patterns"]
"""
    )

    formatted = prompt.format_messages(
        columns=", ".join(columns),
        rows=rows[:5]
    )

    llm = GroqChatLLM()
    response = llm(formatted)

    text = response.content.strip()

    try:
        categories = eval(text)
        if isinstance(categories, list):
            return categories
        else:
            return ["Performance & Accuracy Insights", "Learning Patterns", "Demographic Trends", "Engagement Analysis", "Comparative Performance", "Visualization Insights"]
    except Exception:
        return ["Performance & Accuracy Insights", "Learning Patterns", "Demographic Trends", "Engagement Analysis", "Comparative Performance", "Visualization Insights"]
        
