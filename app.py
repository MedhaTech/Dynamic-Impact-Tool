import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from utils.file_loader import load_data
from utils.insight_generator import generate_insights
from utils.visualizer import generate_visualizations

st.set_page_config(page_title="LLM Powered Insight Generator", layout="wide")
st.title("Agentic RAG")

if "insights" not in st.session_state:
    st.session_state.insights = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=['.csv', '.xlsx', '.json'])

model_source = st.radio("Select LLM Backend", ["ollama", "groq"], horizontal=True)

if uploaded_file:
    try:
        df = load_data(uploaded_file)
        st.success("File Loaded")
        st.write("Data Preview")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Failed to load the file: {e}")
        st.stop()

    category = st.selectbox("Select Insight Category", (
        "Performance & Accuracy Insights",
        "Question-Specific Insights",
        "Attempt & Behavioral Insights",
        "Comparative & Demographic Insights",
        "Question Design & Learning Insights",
        "Advanced Statistical Insights",
        "Actionable Recommendations"
    ))

    if st.button("Generate Insights"):
        with st.spinner("Generating insights..."):
            insights = generate_insights(df, category, model_source=model_source)
            st.session_state.insights = insights

    if st.session_state.insights:
        st.markdown("Insights")
        formatted_insights = st.session_state.insights.replace(". ", ".\n")
        st.text(formatted_insights)

    st.markdown("Visualizations")
    charts = generate_visualizations(df)
    for chart in charts:
        st.plotly_chart(chart, use_container_width=True)

    st.markdown("Ask AI About This Data")
    user_input = st.text_input("Ask a question:")
    if st.button("Ask"):
        from utils.groq_handler import query_groq
        response = query_groq(f"User question: {user_input}\n\nBased on this dataset: {df.head(10).to_markdown()}")
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", response))

    for role, text in st.session_state.chat_history:
        st.write(f"**{role.upper()}:** {text}")
