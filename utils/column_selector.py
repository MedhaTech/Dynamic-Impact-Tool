import pandas as pd
import json
from io import StringIO
from langchain_core.messages import HumanMessage
from .llm_selector import get_llm


def get_important_columns(csv_data: str, model_source="groq") -> list:
    """Returns most relevant columns for analysis as a list of strings."""
    df = pd.read_csv(StringIO(csv_data))
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, df.nunique(dropna=True) > 1]

    preview = df.head(100).to_csv(index=False)
    prompt = f"""
You are a senior data analyst. Based on the dataset preview below, suggest the most important columns for analysis.

Return only a Python list: ['col1', 'col2', ...]
Dataset:
{preview[:1200]}
"""

    llm = get_llm(model_source)

    try:
        response = llm.invoke(prompt).content.strip() if hasattr(llm, "invoke") else llm(prompt)
        cols = eval(response)
        if isinstance(cols, list) and all(isinstance(col, str) for col in cols):
            return cols
        return df.columns[:7].tolist()
    except Exception:
        return df.columns[:7].tolist()


def suggest_chart_fields(df: pd.DataFrame, model_source="groq") -> dict:
    """Suggest best x, y, and optional group_by columns for plotting."""
    preview = df.head(100).to_csv(index=False)
    prompt = f"""
You are a helpful data analyst. Given the following dataset preview, suggest the best columns for:

- X-axis
- Y-axis
- Grouping (optional)

Return as JSON:
{{ "x": "column_name", "y": "column_name", "group_by": "column_name" }}

Dataset Preview:
{preview[:3000]}
"""

    llm = get_llm(model_source)

    try:
        result = llm([HumanMessage(content=prompt)]).content
        return json.loads(result)
    except Exception:
        return {"x": None, "y": None, "group_by": None}