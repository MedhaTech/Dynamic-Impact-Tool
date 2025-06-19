# from utils.prompt_engine import build_prompt
# from models.local_model import generate_response

# def genearte_insights(dataframe,category):
#     data_summary = f"Columns : {list(dataframe.columns)}. Total Rows : {len(dataframe)}\n"
#     prompt = build_prompt(category,data_summary)
#     response = generate_response(prompt)
#     return response

# utils/insight_generator.py

from utils.groq_handler import call_groq_model
from utils.ollama_handler import call_ollama_model

def generate_insights(df, category, model_source="groq"):
    columns = ", ".join(df.columns.tolist())
    sample_data = df.head(3).to_dict(orient="records")

    system_prompt = "You are a senior data scientist. Never return code."
    user_prompt = f"Generate {category} from the following dataset:\n\nColumns: {columns}\n\nSample: {sample_data}"

    if model_source == "groq":
        return call_groq_model(system_prompt, user_prompt)
    else:
        return call_ollama_model(system_prompt, user_prompt)
