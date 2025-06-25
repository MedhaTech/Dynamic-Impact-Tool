import pandas as pd
from io import StringIO
from .llm_selector import get_llm
import json

DEFAULT_INSIGHTS = [
    {"title": "Most Frequent Category", "description": "Shows the most common category in a column."},
    {"title": "Distribution of Numerical Features", "description": "Displays how numerical columns are distributed."},
    {"title": "Missing Value Analysis", "description": "Identifies columns with missing data."},
    {"title": "Top Performing Group", "description": "Finds the group with highest average values."},
    {"title": "Correlation Insights", "description": "Shows correlations between numerical variables."},
    {"title": "Outlier Detection", "description": "Highlights values that deviate significantly from the norm."},
    {"title": "Trend Over Time", "description": "Explores how a metric changes across a time column."},
]

def suggest_insight_options_explained(csv_data: str, model_source="groq") -> list:
    df = pd.read_csv(StringIO(csv_data))
    preview = df.head(50).to_csv(index=False)
    llm = get_llm(model_source)

    prompt = f"""
You are a senior data scientist. Here's a sample of the dataset:

{preview[:1200]}

Based on the above dataset, suggest 5 to 7 specific insights a user may want to explore. Each item should have:
- title: short insight title
- description: brief explanation of the insight

Return your answer as a **valid JSON array** like:
[
  {{ "title": "Average Sales by Region", "description": "Shows average sales across regions." }},
  ...
]

Do NOT add any extra text before or after. Only return the JSON list.
"""

    try:
        response = llm.invoke(prompt).content.strip() if hasattr(llm, "invoke") else llm(prompt).strip()

        insights = json.loads(response)

        if isinstance(insights, list) and all("title" in i and "description" in i for i in insights):
            return insights
        else:
            print(" JSON structure invalid. Using default insights.")
            return DEFAULT_INSIGHTS
    except Exception as e:
        print(f"[LLM/JSON Error] {e}")
        # return DEFAULT_INSIGHTS
