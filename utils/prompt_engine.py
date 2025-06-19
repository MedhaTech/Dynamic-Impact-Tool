from langchain.prompts import PromptTemplate

SYSTEM_PROMPT = """"
You are a highly experienced Senior Data Scientist. Generate Structured, exper-level 
inisights based on a categorized these. Avoid generic advice and stick to the dataset context
"""

INSIGHT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=['category','data_summary'],
    template="""
{system_prompt}
You are a visualization planner. DO NOT write Python code.

Your job is to extract chart intent from the user's question and respond ONLY in JSON format.

Required keys:
- chart_type: one of ["bar", "line", "scatter", "pie", "box"]
- group_by: a list of column names to compare (e.g., ["heart_disease", "stroke"])

Return only the chart type and group_by fields
Based on the Following Category :{category}
and the dataset summary : {data_summary}

generate 10 insights for the selected category.number them and keep them concise and factual.
"""
)


def build_prompt(category,data_summary):
    return INSIGHT_PROMPT_TEMPLATE.format(
        category=category,
        data_summary=data_summary,
        system_prompt = SYSTEM_PROMPT
    )