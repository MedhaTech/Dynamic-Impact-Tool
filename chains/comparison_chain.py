from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY

class GroqChatLLM(ChatOpenAI):
    def __init__(self, model="llama3-8b-8192", temperature=0.3, **kwargs):
        super().__init__(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )

def compare_datasets(df1_cols, df2_cols, df1_rows, df2_rows):
    prompt = ChatPromptTemplate.from_template(
        """You are a professional data scientist.

Compare these two datasets based on their columns and sample data:

**Dataset A**
Columns: {cols1}
Sample Rows: {rows1}

**Dataset B**
Columns: {cols2}
Sample Rows: {rows2}

Write a comparison report:
- Similarities
- Differences
- Common variables
- Structure, patterns, trends

Return in structured markdown format.
"""
    )

    messages = prompt.format_messages(
        cols1=", ".join(df1_cols),
        cols2=", ".join(df2_cols),
        rows1=df1_rows[:5],
        rows2=df2_rows[:5]
    )

    llm = GroqChatLLM()
    response = llm(messages)

    return response.content.strip()

# import streamlit as st
# from langchain.prompts import ChatPromptTemplate
# from chains.llms import GroqChatLLM

# def generate_llm_diff_summary(df1, df2, column):
#     prompt = ChatPromptTemplate.from_template(
#         """
# You are a data analyst.

# Compare this column: "{column}"

# Dataset A values (sample): {values1}
# Dataset B values (sample): {values2}

# Summarize key differences in distribution, range, or patterns in 3–5 bullet points.
# Use numbers if possible. Be concise.
# """
#     )

#     try:
#         values1 = df1[column].dropna().astype(str).sample(min(100, len(df1))).tolist()
#         values2 = df2[column].dropna().astype(str).sample(min(100, len(df2))).tolist()

#         llm = GroqChatLLM()
#         messages = prompt.format_messages(column=column, values1=values1, values2=values2)
#         response = llm(messages)

#         return response.content.strip()
#     except Exception as e:
#         print("❌ Comparison summary failed:", e)
#         return "Could not generate comparison summary."
