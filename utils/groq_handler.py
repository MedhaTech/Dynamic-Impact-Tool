import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# def query_groq(prompt):
#     from openai import OpenAI
#     import os

#     client = OpenAI(
#         api_key=os.getenv("GROQ_API_KEY"),
#         base_url="https://api.groq.com/openai/v1"
#     )

#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": "You are a senior data scientist."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.5,
#         max_tokens=1024,
#     )
#     return response.choices[0].message.content.strip()


from langchain_groq import ChatGroq
from config import GROQ_API_KEY

llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192")

def call_groq_model(system_prompt, query_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query_prompt}
    ]
    response = llm.invoke(messages)
    return response.content.strip()
