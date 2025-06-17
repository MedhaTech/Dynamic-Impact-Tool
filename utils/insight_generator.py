# from utils.prompt_engine import build_prompt
# from models.local_model import generate_response

# def genearte_insights(dataframe,category):
#     data_summary = f"Columns : {list(dataframe.columns)}. Total Rows : {len(dataframe)}\n"
#     prompt = build_prompt(category,data_summary)
#     response = generate_response(prompt)
#     return response

from utils.ollama_handler import query_ollama
from utils.groq_handler import query_groq

def generate_insights(df, category, model_source="ollama"):
    prompt = f"Generate top 10 advanced insights in one paragraph format for this category: {category}\n\nData Preview:\n{df.head(10).to_markdown()}"

    if model_source == "groq":
        return query_groq(prompt)  
    elif model_source == "ollama":
        return query_ollama(prompt)  
    else:
        raise ValueError("Invalid model_source: choose 'ollama' or 'groq'")
