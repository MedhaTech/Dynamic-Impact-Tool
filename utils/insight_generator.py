from .llm_selector import get_llm
import pandas as pd
import json
import ast

# Generates suggestions for insight titles + descriptions
def generate_insight_suggestions(csv_text: str, model_source="groq"):
    prompt = f"""
You are a helpful data analyst.

Analyze the dataset preview below and suggest 5 smart insights a user might explore.

Dataset Preview (CSV Format):
{csv_text[:3000]}

For each suggestion, return a title and a short explanation.

Return strictly as JSON:
[
  {{"title": "Insight Title 1", "description": "Short explanation."}},
  ...
]
"""
    llm = get_llm(model_source)
    result = llm(prompt)
    try:
        return json.loads(result)
    except:
        try:
            return ast.literal_eval(result)
        except Exception as e:
            return [{"title": "Insight generation failed", "description": str(e)}]

# Generates full insight based on selected title
def generate_insights(df: pd.DataFrame, insight_title: str, model_source="groq") -> str:
    preview = df.head(100).to_csv(index=False)
    prompt = f"""
You are a senior data analyst. Based on the following dataset preview and the selected insight, generate 4 to 6 concise, bullet-pointed insights.

Dataset:
{preview[:3000]}

Selected Insight: {insight_title}

Each bullet should highlight a clear data-driven observation. Keep language simple, avoid technical jargon, and DO NOT include Python code.

Respond in **markdown-friendly bullet points** like:
- Observation 1
- Observation 2
...
"""
    llm = get_llm(model_source)
    return llm(prompt)
