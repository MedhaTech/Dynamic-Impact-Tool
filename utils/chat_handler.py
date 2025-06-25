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
from datetime import datetime
from .ollama_handler import call_ollama_model
from .groq_handler import call_groq_model
from .logger import logger


def handle_user_query_dynamic(user_query, df, model_source="groq"):
    schema = ", ".join(df.columns.tolist())
    preview = df.head(3).to_dict(orient='records')

    system_prompt = """
You are a Senior Data Analyst Agent. You never return Python code.
If the user's question is about a chart, return only:
{
  "response": {
    "chart_type": "bar", 
    "group_by": ["column1", "column2"]
  },
  "follow_ups": ["suggested question 1", "suggested question 2"]
}
If it's a data insight, return only:
{
  "response": "Plain text answer",
  "follow_ups": ["suggested question 1", "suggested question 2"]
}
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

        try:
            parsed = json.loads(output)
            return parsed
        except Exception as parse_error:
            logger.warning(f"[JSON Parse Fallback] {parse_error}")
            return {
                "response": output.strip(),
                "follow_ups": []
            }

    except Exception as e:
        logger.error(f"[LLM Error] {e}")
        return {
            "response": f"LLM Error: {e}",
            "follow_ups": []
        }
