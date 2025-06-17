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


from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOllama

llm = ChatOllama(model="gemma:2b")  

def handler_chat(user_question, df, insights=None):
    from pandas import DataFrame

    df_sample = df.head(20).to_csv(index=False)

    prompt = f"""
You are a data analyst. You are provided with a dataset sample:
{df_sample}

And the following insights if available:
{insights or "None"}

Answer this question based on the dataset: {user_question}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Error: {e}"


