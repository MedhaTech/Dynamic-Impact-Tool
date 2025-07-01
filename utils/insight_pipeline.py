import pandas as pd
import json
from utils.llm_selector import get_llm
from utils.insight_suggester import get_important_columns
from utils.insight_generator import generate_insights


def generate_full_insight(df: pd.DataFrame, insight_type: str, model_source="groq"):
    """
    Handles full insight generation pipeline:
    - Selects important columns
    - Generates insight from LLM
    - Parses optional chart suggestion
    """
    preview = df.head(100).to_csv(index=False)

    # Step 1: Column suggestion (optional, but makes LLM smarter)
    selected_cols = get_important_columns(preview, model_source)

    # Step 2: Insight generation from LLM
    raw_response = generate_insights(df, insight_type, model_source)

    # Step 3: Try to parse insight + chart_suggestion from JSON
    try:
        parsed = json.loads(raw_response)
        insight = parsed.get("insight", "⚠️ Insight missing.")
        chart = parsed.get("chart_suggestion", None)
    except:
        insight = raw_response
        chart = None

    return insight, chart, selected_cols
