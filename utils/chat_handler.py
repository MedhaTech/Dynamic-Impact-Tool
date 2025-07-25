from utils.groq_handler import call_groq_model, call_ollama_model
from utils.logger import logger
import json
import traceback
import ast

def handle_user_query_dynamic(prompt, df, model_source="groq"):
    try:
        preview = df.head(100).to_csv(index=False)

        system_prompt = """
You are a senior data analyst.
Your task is to answer the user's question based on a preview of the dataset.
Respond clearly and concisely.

If relevant, return a JSON object in this format:
{
  "response": "Textual insight or answer here",
  "chart_type": "bar | line | scatter | pie | box | violin | area",
  "group_by": ["column1", "column2"],
  "title": "Optional chart title"
}

If no chart is needed, return just the text insight as a string.
        """

        user_prompt = f"""
User Question: {prompt}

Dataset Preview:
{preview[:1500]}
        """

        logger.info(f"[Model: {model_source}] Prompt: {prompt}")

        if model_source == "groq":
            response = call_groq_model(system_prompt, user_prompt)
        else:
            response = call_ollama_model(f"{system_prompt.strip()}\n{user_prompt.strip()}")

        logger.info(f"[LLM Raw Response]: {response}")

        # Try parsing response
        try:
            parsed = json.loads(response)
            return parsed if isinstance(parsed, dict) else {"response": response}
        except json.JSONDecodeError:
            try:
                parsed = ast.literal_eval(response)
                return parsed if isinstance(parsed, dict) else {"response": response}
            except Exception:
                return {"response": response}

    except Exception as e:
        logger.error(f"Exception in handle_user_query_dynamic: {e}")
        traceback.print_exc()
        return {"response": "An error occurred while processing your request."}
