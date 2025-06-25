# from utils.prompt_engine import build_prompt
# from models.local_model import generate_response

# def genearte_insights(dataframe,category):
#     data_summary = f"Columns : {list(dataframe.columns)}. Total Rows : {len(dataframe)}\n"
#     prompt = build_prompt(category,data_summary)
#     response = generate_response(prompt)
#     return response



from .llm_selector import get_llm
import pandas as pd
from io import StringIO

def generate_insights(df: pd.DataFrame, insight_title: str, model_source="groq") -> str:
    preview = df.head(100).to_csv(index=False)

    prompt = f"""
You are a senior data scientist. Based on the following dataset preview and the selected insight:

Dataset:
{preview[:3000]}

Selected Insight: {insight_title}

Generate a detailed data insight. Do not include Python code. Keep it simple and data-driven.
"""

    llm = get_llm(model_source)
    return llm(prompt)

