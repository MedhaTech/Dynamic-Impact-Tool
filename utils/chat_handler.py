# from models.local_model import generate_response

# CHAT_PROMPT_TEMPLATE = """
# You are a senior data scientist. Answer the user's query using the upoaded dataset's context
# Be Specfic , insightful , and brief
# User Question:{user_input}
# """

# def handler_chat(user_input,insight_context):
#     prompt = CHAT_PROMPT_TEMPLATE.format(
#         insight_context=insight_context,
#         user_input=user_input
#     )
#     return generate_response(prompt)

import json
from utils.ollama_handler import call_ollama_model
from utils.groq_handler import call_groq_model
from utils.logger import logger
from utils.groq_handler import call_groq_model



def handle_user_query_dynamic(user_query, df, model_source="groq"):
    schema = ", ".join(df.columns.tolist())
    preview = df.head(3).to_dict(orient='records')

    system_prompt = """
You are a Senior Data Analyst Agent. You never return Python code.
If the user's question is about a chart, return only:
{
  "chart_type": "bar", 
  "group_by": ["heart_disease", "stroke"]
}

If the user's question is about a data insight, return the answer in plain text. Do NOT generate any charts unless explicitly asked.
"""

    query_prompt = f"""Dataset Columns: {schema}
Sample Data: {preview}
User Query: {user_query}"""

    try:
        logger.info(f"[User Query] {user_query}")
        logger.info(f"[Columns] {schema}")
        logger.info(f"[Model Source] {model_source}")

        if model_source == "groq":
            output = call_groq_model(system_prompt, query_prompt)
        else:
            output = call_ollama_model(system_prompt, query_prompt)

        logger.info(f"[LLM Raw Output] {output}")

        # Try parsing chart-type response
        try:
            parsed = json.loads(output)
            logger.info(f"[Parsed LLM Response] {parsed}")
            return parsed
        except Exception as parse_error:
            logger.warning(f"[Fallback to Text Response] Could not parse JSON: {parse_error}")
            return output.strip()

    except Exception as e:
        logger.error(f"[LLM Error] {e}")
        return f"LLM Error: {e}"
