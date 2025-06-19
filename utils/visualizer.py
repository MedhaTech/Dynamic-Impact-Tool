# import plotly.express as px

# def generate_visualization(df):
#     visualization = []

#     for column in df.select_dtypes(include='number').columns:
#         fig = px.histogram(df,x=column,title=f"Distribution of {column}")
#         visualization.append(fig)
    
#     for column in df.select_dtypes(include='object').columns:
#         top_values = df[column].value_counts().nlargest(10).reset_index()
#         if not top_values.empty:
#             top_values.columns = ['value', 'count'] 
#             fig = px.bar(top_values, x='value', y='count', title=f"Top Values in {column}")     
#     return  visualization


import pandas as pd
import plotly.express as px
import streamlit as st

def generate_group_comparison_chart(df, chart_type, group_by):
    try:
        data = {}
        for col in group_by:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found.")

            if df[col].dtype in ['bool', 'int', 'float'] and set(df[col].dropna().unique()) <= {0, 1}:
                data[col.replace("_", " ").title()] = int(df[col].sum())
            else:
                data[col.replace("_", " ").title()] = df[col].value_counts().iloc[0]

        chart_df = pd.DataFrame({
            "Condition": list(data.keys()),
            "Count": list(data.values())
        })

        if chart_type == "bar":
            return px.bar(chart_df, x="Condition", y="Count", title="Condition Comparison")
        elif chart_type == "pie":
            return px.pie(chart_df, names="Condition", values="Count", title="Condition Breakdown")
        else:
            raise ValueError("Unsupported chart type.")

    except Exception as e:
        st.error(f"[Chart Error]: {e}")
        return None

def visualize_from_llm_response(df, user_query, llm_response):
    try:
        if not llm_response or not isinstance(llm_response, dict):
            return None

        chart_type = llm_response.get("chart_type", "bar")
        group_by = llm_response.get("group_by", [])

        if not group_by:
            return None

        return generate_group_comparison_chart(df, chart_type, group_by)

    except Exception as e:
        st.error(f"[LLM Visualization Error]: {e}")
        return None
