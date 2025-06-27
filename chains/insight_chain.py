from langchain.prompts import ChatPromptTemplate
from chains.category_chain import GroqChatLLM
def generate_insights_for_category(columns, rows, category):
    prompt = ChatPromptTemplate.from_template(
        """You are a highly skilled data scientist.

Based on this dataset:
Columns: {columns}
Sample Rows: {rows}

Now, under the category **"{category}"**, generate 5–10 detailed insights or observations using the data. 
Return:
- Realistic insights
- Use numbers/percentages if visible
- Mention visual patterns if relevant
- Avoid code. Just insight explanations (markdown ok)
"""
    )

    formatted = prompt.format_messages(
        columns=", ".join(columns),
        rows=rows[:5],
        category=category
    )

    llm = GroqChatLLM()
    response = llm(formatted)

    return response.content.strip()




