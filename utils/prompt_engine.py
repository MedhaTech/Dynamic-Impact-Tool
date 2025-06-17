from langchain.prompts import PromptTemplate

SYSTEM_PROMPT = """"
You are a highly experienced Senior Data Scientist. Generate Structured, exper-level 
inisights based on a categorized these. Avoid generic advice and stick to the dataset context
"""

INSIGHT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=['category','data_summary'],
    template="""
{system_prompt}
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