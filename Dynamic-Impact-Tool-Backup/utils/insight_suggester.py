<<<<<<< HEAD
import json
from utils.groq_handler import call_groq_model  

def suggest_insight_options_explained(csv_data, model_source="groq"):
    """
    Uses LLM to suggest 5 meaningful data insights based on CSV data.
    Returns a list of dictionaries with 'title' and 'description'.
    """
    prompt = f"""
You are a data insights assistant.

Given a dataset in CSV format, generate 5 helpful insights a data analyst might explore.

Respond in valid JSON format as a list like this:
[
  {{
    "title": "Insight Title",
    "description": "What this insight reveals and why it's useful"
  }},
  ...
]

Here is the dataset:
{csv_data[:2000]}
=======
from langchain_core.messages import HumanMessage
from .llm_selector import get_llm
import json, ast
import pandas as pd

def generate_insight_suggestions(csv_text: str, model_source="groq"):
    from .llm_selector import get_llm
    import json, ast

    prompt = f"""
You are a helpful data analyst.

Analyze the dataset preview below and suggest 5 smart comparison insights a user might explore between two datasets.

Dataset Preview (CSV Format):
{csv_text[:3000]}

For each suggestion, return a title and a short explanation.

Respond strictly as a JSON list:
[
  {{"title": "Insight Title 1", "description": "Short explanation."}},
  ...
]
>>>>>>> e1bab98 (Modified the code)
"""

    llm = get_llm(model_source)
    result = llm([HumanMessage(content=prompt)])

    if hasattr(result, "content"):
        result_text = result.content
    else:
        result_text = result  

    try:
<<<<<<< HEAD
        raw_response = call_groq_model(prompt)  
        
        if "```json" in raw_response:
            content = raw_response.split("```json")[-1].split("```")[0].strip()
        elif "```" in raw_response:
            content = raw_response.split("```")[1].strip()
        else:
            content = raw_response.strip()

        suggestions = json.loads(content)

        if isinstance(suggestions, list) and all("title" in i and "description" in i for i in suggestions):
            return suggestions
        else:
            raise ValueError("Invalid insight format")

    except Exception as e:
        print("Failed to parse insight suggestions:", e)
        return []
=======
        return json.loads(result_text)
    except Exception:
        try:
            return ast.literal_eval(result_text)
        except Exception as e:
            return [{"title": "Insight generation failed", "description": str(e)}]


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
    return llm([HumanMessage(content=prompt)]).content  # ✅ FIXED


def suggest_insight_options_explained(df):
    return [
        {"title": "Performance & Accuracy Insights", "description": "Analyze performance trends, accuracy rates, and scoring patterns."},
        {"title": "Question-Specific Insights", "description": "Dive deep into patterns for specific questions or categories."},
        {"title": "Attempt & Behavioral Insights", "description": "Explore attempt behaviors, skipping patterns, or answer changes."},
        {"title": "Comparative & Demographic Insights", "description": "Compare performance across groups, like gender, location, or age."},
        {"title": "Question Design & Learning Insights", "description": "Understand question clarity, difficulty, or learning outcomes."},
        {"title": "Advanced Statistical Insights", "description": "Surface correlations, regressions, or multi-variate findings."},
        {"title": "Actionable Recommendations", "description": "Suggest actions based on detected patterns and issues."}
    ]

def generate_comparison_insights(df: pd.DataFrame, insight_title: str, model_source="groq") -> str:
    preview = df.head(100).to_csv(index=False)
    prompt = f"""
You are a senior data analyst. Compare the two datasets based on the following data preview and the selected insight category. Provide clear differences, trends, or similarities.

Dataset (with 'Source' column identifying the dataset origin):
{preview[:3000]}

Comparison Insight: {insight_title}

Return 4–6 bullet-pointed observations in simple language.

- Observation 1
- Observation 2
...
"""
    llm = get_llm(model_source)
    return llm([HumanMessage(content=prompt)]).content
>>>>>>> e1bab98 (Modified the code)
