def quick_dataframe_comparison(df1, df2):
    comparison = {
        "rows_a": df1.shape[0],
        "cols_a": df1.shape[1],
        "rows_b": df2.shape[0],
        "cols_b": df2.shape[1],
        "common_columns": list(set(df1.columns).intersection(set(df2.columns))),
        "unique_to_a": list(set(df1.columns) - set(df2.columns)),
        "unique_to_b": list(set(df2.columns) - set(df1.columns))
    }
    return comparison


# import streamlit as st
# import plotly.express as px

# def render_comparison_charts(df1, df2, chart_type, column):
#     st.markdown(f"### 📊 Comparing `{column}` — Dataset A vs Dataset B")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("**Dataset A**")
#         fig1 = generate_chart(df1, chart_type, column)
#         st.plotly_chart(fig1, use_container_width=True)

#     with col2:
#         st.markdown("**Dataset B**")
#         fig2 = generate_chart(df2, chart_type, column)
#         st.plotly_chart(fig2, use_container_width=True)

# def generate_chart(df, chart_type, col):
#     if chart_type == "bar":
#         return px.bar(df[col].value_counts().reset_index(), x="index", y=col, labels={"index": col})
#     elif chart_type == "histogram":
#         return px.histogram(df, x=col)
#     elif chart_type == "box":
#         return px.box(df, y=col)
#     else:
#         return px.histogram(df, x=col)
