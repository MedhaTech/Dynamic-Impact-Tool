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


import plotly.express as px

def visualize_from_llm_response(df, query, llm_response):
    try:
        chart_type = llm_response.get("chart_type")
        group_by = llm_response.get("group_by")

        if not group_by:
            return None

        if chart_type == "bar":
            return px.bar(df, x=group_by[0], y=group_by[1] if len(group_by) > 1 else None)
        elif chart_type == "scatter":
            return px.scatter(df, x=group_by[0], y=group_by[1])
        elif chart_type == "line":
            return px.line(df, x=group_by[0], y=group_by[1])
        elif chart_type == "histogram":
            return px.histogram(df, x=group_by[0])
        elif chart_type == "box":
            return px.box(df, x=group_by[0], y=group_by[1] if len(group_by) > 1 else None)
        else:
            return None

    except Exception as e:
        return None
