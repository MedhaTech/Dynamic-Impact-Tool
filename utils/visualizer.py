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

def generate_visualizations(df):
    visualizations = []

    for column in df.select_dtypes(include='number').columns:
        fig = px.histogram(df, x=column, title=f"Distribution of {column}")
        visualizations.append(fig)

    for column in df.select_dtypes(include='object').columns:
        top_values = df[column].value_counts().nlargest(10).reset_index()
        if not top_values.empty:
            top_values.columns = ['value', 'count']
            fig = px.bar(top_values, x='value', y='count', title=f"Top Values in {column}")
            visualizations.append(fig)

    return visualizations

