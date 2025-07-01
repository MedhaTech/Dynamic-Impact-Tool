from .groq_handler import call_groq_model
from .ollama_handler import call_ollama_model
from .logger import logger
import json

def compare_datasets_with_llm(df1, df2, model_source="groq"):
    schema1 = df1.dtypes.apply(str).to_dict()
    schema2 = df2.dtypes.apply(str).to_dict()
    sample1 = df1.head(3).to_dict(orient='records')
    sample2 = df2.head(3).to_dict(orient='records')

    system_prompt = """
You are a Senior Data Scientist.
Your job is to compare two datasets in terms of:
- Schema differences (columns, datatypes)
- Sample data patterns
- Possible insights or red flags

Return a well-formatted text explanation.
    """

    query_prompt = f"""
Dataset 1 Schema: {schema1}
Dataset 1 Sample: {sample1}

Dataset 2 Schema: {schema2}
Dataset 2 Sample: {sample2}

Compare both datasets.
    """

    try:
        logger.info("Comparing two datasets using LLM")
        if model_source == "groq":
            output = call_groq_model(system_prompt, query_prompt)
        else:
            output = call_ollama_model(system_prompt, query_prompt)
        return output.strip()
    except Exception as e:
        logger.error(f"Dataset comparison failed: {e}")
        return f"Error comparing datasets: {e}"
