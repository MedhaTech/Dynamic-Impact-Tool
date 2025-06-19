import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from utils.file_loader import load_data
from utils.insight_generator import generate_insights
from utils.chat_handler import handle_user_query_dynamic
from utils.visualizer import visualize_from_llm_response

st.set_page_config(page_title="LLM Powered Insight Generator", layout="wide")
st.title("Know your Data")

if "insights" not in st.session_state:
    st.session_state.insights = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload CSV / Excel / JSON", type=['.csv', '.xlsx', '.json'])

model_source = "groq"  # or "ollama"
st.info(f"Using Model Backend: {model_source.upper()}")

if uploaded_file:
    try:
        df = load_data(uploaded_file)
        st.success("File Loaded Successfully")
        st.subheader("Data Preview")
        st.dataframe(df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        st.stop()

    st.subheader("Select Insight Category")
    category = st.selectbox("Insight Type", (
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
        st.markdown("### Generated Insights")
        st.text(st.session_state.insights)

    st.subheader("Talk to your Data")
    user_input = st.chat_input("Ask a question or request a chart...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                response = handle_user_query_dynamic(user_input, df, model_source=model_source)

                if isinstance(response, dict) and "chart_type" in response:
                    fig = visualize_from_llm_response(df, user_input, response)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Chart generation failed. Please try another query.")
                else:
                    st.markdown(response)
            except Exception as e:
                st.error(f"Agent failed: {e}")
