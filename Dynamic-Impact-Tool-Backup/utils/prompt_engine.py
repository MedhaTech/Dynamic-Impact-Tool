from langchain.prompts import PromptTemplate

# System role description
SYSTEM_PROMPT = """
You are a highly experienced and detail-oriented Data Analyst and Data Storyteller. 
Based on the user's query and dataset summary, respond with an analytical, helpful, and clear answer. 
Include insight, reasoning, and if applicable, chart instructions (chart_type and group_by).
Avoid generic responses.
"""

# === Chat Prompt Template ===
CHAT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["user_query", "data_summary"],
    template="""
{system_prompt}

Dataset Summary:
{data_summary}

User Question:
{user_query}

Respond with analysis, insights, and if needed chart_type and group_by.
"""
)

def build_chat_prompt(user_query: str, data_summary: str) -> str:
    return CHAT_PROMPT_TEMPLATE.format(
        system_prompt=SYSTEM_PROMPT,
        user_query=user_query,
        data_summary=data_summary
    )


# === Insight Prompt (Optional if using insight_suggester) ===
INSIGHT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["category", "data_summary"],
    template="""
{system_prompt}

You are a senior data analyst. Based on the selected category and dataset summary below,
generate 10 concise, useful, and factual insights.

Category: {category}
Dataset Summary: {data_summary}

Number and list each insight separately.
"""
)

def build_insight_prompt(category: str, data_summary: str) -> str:
    return INSIGHT_PROMPT_TEMPLATE.format(
        system_prompt=SYSTEM_PROMPT,
        category=category,
        data_summary=data_summary
    )
