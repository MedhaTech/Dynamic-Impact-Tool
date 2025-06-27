import ast
import streamlit as st
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

def generate_visual_suggestions(df):
    prompt = ChatPromptTemplate.from_template(
        """
You are a data analyst.

You will be given:
- A list of column names: {columns}
- The column data types: {types}
- A few sample rows: {rows}

Your task:
Suggest 3 to 5 visualizations the user can create.

Return a valid Python list of dicts. Each dict must contain:
{
  "insight": "...",
  "chart": {"type": "bar/line/scatter/histogram/pie", "x": "col1", "y": "col2 (optional)"}
}

✅ Wrap everything in [ ... ]
❌ Do not return anything before/after the list
❌ No markdown, numbering, or explanations

Example:
[
  {
    "insight": "Sales increase over months.",
    "chart": { "type": "line", "x": "month", "y": "sales" }
  }
]
"""
    )


    sample_rows = df.head(3).to_dict(orient="records")
    types = df.dtypes.apply(lambda x: str(x)).to_dict()
    llm = GroqChatLLM()

    try:
        messages = prompt.format_messages(
            columns=", ".join(df.columns),
            types=types,
            rows=sample_rows
        )

        response = llm(messages)

        if not hasattr(response, "content"):
            raise ValueError("No content in LLM response.")

        raw = response.content.strip()
        st.session_state["last_llm_visual_raw"] = raw
        print("🧠 Raw LLM Visual Suggestion Output:\n", raw)

        # Try to parse the LLM response safely
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return parsed

    except Exception as e:
        print("❌ Failed to parse LLM visual suggestions.")
        print("Error:", e)
        print("LLM raw output:\n", raw if 'raw' in locals() else "No response.")

        st.session_state["last_llm_visual_raw"] = raw if 'raw' in locals() else "❌ No valid content"

    return [{"insight": "No valid visual suggestions were returned.", "chart": None}]
