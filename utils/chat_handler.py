from utils.llm_selector import get_llm

def handle_user_query_dynamic(user_prompt, df, model_source="groq"):
    preview = df.head(50).to_csv(index=False)

    prompt = f"""
You are a senior data scientist.
Here is a dataset preview:
{preview[:1200]}

User asked: {user_prompt}

Respond with a concise insight or answer. If suitable, include chart metadata in the format:
{{
  "response": "...",
  "chart_type": "bar",
  "x": "column_x",
  "y": "column_y",
  "group_by": ["col1"],
  "title": "Chart Title",
  "follow_ups": ["suggested followup 1", "another followup"]
}}
"""

    llm = get_llm(model_source)
    try:
        response = llm.invoke(prompt).content.strip() if hasattr(llm, "invoke") else llm(prompt)
        return eval(response) if response.startswith("{") else {"response": response}
    except Exception as e:
        print("LLM Chat Error:", e)
        return {"response": "⚠️ Error generating insight."}

from utils.llm_selector import get_llm
from utils.prompt_engine import build_chat_prompt
from utils.error_handler import safe_llm_call

# # 🧠 General LLM Response Handler
# def handle_user_query_dynamic(user_query: str, df, model_source="groq"):
#     prompt = build_chat_prompt(user_query, df)
#     llm = get_llm(model_source)

#     try:
#         if hasattr(llm, "invoke"):
#             response = llm.invoke(prompt).content.strip()
#         else:
#             response = llm(prompt)
#     except Exception as e:
#         return {"response": f"⚠️ LLM Error: {e}"}

#     try:
#         result = eval(response) if isinstance(response, str) and response.startswith("{") else {"response": response}
#         if isinstance(result, dict):
#             return result
#         else:
#             return {"response": str(result)}
#     except Exception:
#         return {"response": response}


# 🧪 Raw Prompt Handler (Optional)
def generate_chat_response(prompt, model_source="groq"):
    llm = get_llm(model_source)
    return safe_llm_call(lambda p: llm.invoke(p).content.strip() if hasattr(llm, "invoke") else llm(p), prompt, default="⚠️ LLM error.")

# 💬 For Real-Time Chat (Future: stream support)
def handle_chat_query(user_input: str, df, model_source="groq"):
    return handle_user_query_dynamic(user_input, df, model_source)
