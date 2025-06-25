import pandas as pd
from io import StringIO
from utils.llm_selector import get_llm

def get_important_columns(csv_data: str, model_source="groq") -> list:
    df = pd.read_csv(StringIO(csv_data))

    df = df.dropna(axis=1, how='all')

    df = df.loc[:, df.nunique(dropna=True) > 1]

    preview = df.head(100).to_csv(index=False)

    prompt = f"""
You are a senior data analyst. Based on the dataset preview below, suggest the most important columns for data analysis or visualization.

Return only the column names in a Python list format like: ['Age', 'Score', 'Category']
Dataset preview:
{preview[:1200]}
"""
    llm = get_llm(model_source)

    try:
        if hasattr(llm, "invoke"):
            response = llm.invoke(prompt).content.strip()
        else:
            response = llm(prompt)

        cols = eval(response)
        if isinstance(cols, list) and all(isinstance(col, str) for col in cols):
            return cols
        else:
            return df.columns[:7].tolist()
    except Exception:
        return df.columns[:7].tolist()
