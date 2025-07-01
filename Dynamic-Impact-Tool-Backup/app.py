import streamlit as st
from dotenv import load_dotenv

from components.sidebar import render_sidebar
from components.summary_section import render_summary_tab
from components.insights_section import render_insights_tab
from components.comparison_section import render_comparison_tab
from components.export_section import render_export_tab

from utils.state_manager import init_session_state

load_dotenv()

st.set_page_config(page_title="Dynamic Impact Tool", layout="wide", page_icon="📊")

init_session_state()

session_defaults = {
    "df": None,                
    "df1": None,              
    "df2": None,             
    "summary_output_1": "",
    "summary_output_2": "",
    "insight_output_1": "",
    "insight_output_2": "",
    "comparison_result": "",
    "compare_chat": [],
    "chat_history": [],
    "visual_suggestions": [],  
}
for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

section = render_sidebar()

if section == "Single Dataset":
    render_summary_tab()
    render_insights_tab()

elif section == "Dataset Comparison":
    render_comparison_tab()

elif section == "Summary & Export":
    render_export_tab()

else:
    st.info("Please select a valid section from the sidebar.")
# app.py (Cleaned - No Unicode Warnings/Emojis)

import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from utils.file_loader import load_data
from utils.data_cleaner import clean_data
from utils.chat_handler import handle_user_query_dynamic
from utils.visualizer import (
    visualize_from_llm_response,
    visualize_comparison_overlay,
    visualize_comparison_side_by_side
)
from utils.pdf_exporter import generate_pdf_report, export_to_pptx
from utils.error_handler import safe_llm_call
from utils.insight_suggester import (
    generate_insight_suggestions,
    generate_insights,
    generate_comparison_insights
)
from utils.column_selector import get_important_columns
from utils.llm_selector import get_llm

load_dotenv()
st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

for key in ["df", "df1", "df2", "insights", "chat_history", "compare_chat"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "chat" in key else None

with st.sidebar:
    st.title("Dynamic Impact Tool")
    section = st.radio("Navigate", ["Upload & Insights", "Compare Datasets", "Summary & Export"], key="sidebar_section")
    model_source = st.selectbox("Model", ["groq", "ollama"], key="sidebar_model")

# === Section 1: Upload & Insights ===
if section == "Upload & Insights":
    st.header("📥 Upload Dataset")

    # 1. Upload CSV/Excel/JSON
    col1, col2 = st.columns(2)
    uploaded_file = col1.file_uploader("Upload CSV / Excel / JSON", type=["csv", "xlsx", "json"], key="upload_main")
    file_path = col2.text_input("Or Enter File Path", key="path_main")

    sample_rows = st.slider("Sample Rows (Preview Limit)", 0, 100, 0, key="sample_rows_upload")
    sample_rows = None if sample_rows == 0 else sample_rows

    file = open(file_path, "rb") if file_path else uploaded_file
    if file:
        df, _ = load_data(file, sample_rows)
        df = clean_data(df)
        st.session_state.df = df
        st.success("Dataset Loaded")
        st.dataframe(df.head(), use_container_width=True)

        # 2. AI-SELECTED COLUMNS
        st.markdown("## 🧠 AI-Selected Important Columns")
        important_cols = get_important_columns(df.to_csv(index=False), model_source=model_source)

        if important_cols:
            st.success(f"AI prioritized {len(important_cols)} important columns.")
            try:
                st.dataframe(df[important_cols].head(), use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying important columns: {e}")
        else:
            st.warning("AI failed to suggest important columns.")

        # 3. MANUAL CHART CONTROLS
        st.markdown("## 📈 Visualization")
        x_axis = st.selectbox("Select X-Axis", important_cols if important_cols else df.columns.tolist(), key="x_axis")
        y_axis = st.selectbox("Select Y-Axis", important_cols if important_cols else df.columns.tolist(), key="y_axis")
        chart_type = st.selectbox("Chart Type", ["bar", "line", "scatter", "box", "violin", "area", "pie"], key="chart_type")

        if x_axis and y_axis and x_axis in df.columns and y_axis in df.columns:
            try:
                llm_response = {
                    "chart_type": chart_type,
                    "x": x_axis,
                    "y": y_axis,
                    "group_by": None
                }
                fig, explanation = visualize_from_llm_response(df, f"{x_axis} vs {y_axis}", llm_response)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption(explanation)
                else:
                    st.warning("No chart could be generated.")
            except Exception as e:
                st.error(f"Visualization failed: {e}")
        else:
            st.info("Please select valid X and Y columns to generate visualization.")

        # 4. AI-SUGGESTED INSIGHTS
        st.markdown("## 🧠 Suggested Insights")
        try:
            preview = df.head(100).to_csv(index=False)
            suggestions = generate_insight_suggestions(preview, model_source)
            titles = [s['title'] for s in suggestions]
        except Exception as e:
            titles = []
            st.warning(f"Insight suggestion failed: {e}")

        if titles:
            selected_title = st.selectbox("Select Insight to Generate", titles)
            if st.button("Generate Insight"):
                try:
                    insight_result = generate_insights(df, selected_title, model_source)
                    st.session_state.insights = {"response": insight_result}
                    st.success("Insight Generated")
                    st.markdown(insight_result)
                except Exception as e:
                    st.error(f"Insight generation failed: {str(e)}")

        # 5. CHAT WITH DATA
        st.markdown("## 💬 Ask Your Data")
        user_prompt = st.chat_input("Ask a question about your dataset...")
        if user_prompt:
            result = safe_llm_call(handle_user_query_dynamic, user_prompt, df, model_source, default={"response": "No response."})
            st.session_state.chat_history.append({"user": user_prompt, "assistant": result})

        for msg in st.session_state.chat_history[::-1]:
            with st.chat_message("user"):
                st.markdown(msg["user"])
            with st.chat_message("assistant"):
                st.markdown(msg["assistant"].get("response", msg["assistant"]))

# === Section 2: Compare Datasets ===
if section == "Compare Datasets":
    st.header("📊 Compare Datasets")
    col1, col2 = st.columns(2)
    uploaded_file1 = col1.file_uploader("Upload Dataset 1", type=["csv", "xlsx", "json"], key="upload_1")
    file_path1 = col1.text_input("Or Enter Path for Dataset 1", key="path_1")


    uploaded_file2 = col2.file_uploader("Upload Dataset 2", type=["csv", "xlsx", "json"], key="upload_2")
    file_path2 = col2.text_input("Or Enter Path for Dataset 2", key="path_2")

    file1 = open(file_path1, "rb") if file_path1 else uploaded_file1
    file2 = open(file_path2, "rb") if file_path2 else uploaded_file2

    df1, df2 = None, None
    if file1 and file2:
        try:
            df1, _ = load_data(uploaded_file1)
            df2, _ = load_data(uploaded_file2)
            df1, df2 = clean_data(df1), clean_data(df2)
            st.session_state.df1, st.session_state.df2 = df1, df2
            st.success("Both datasets loaded successfully.")

            st.subheader("📋 Dataset Previews")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Dataset 1")
                st.dataframe(df1.head(), use_container_width=True)
            with col2:
                st.markdown("#### Dataset 2")
                st.dataframe(df2.head(), use_container_width=True)

            # === AI-Selected Important Columns ===
            st.subheader("🧠 AI-Selected Important Columns")
            col1, col2 = st.columns(2)
            with col1:
                selected_cols1 = get_important_columns(df1.to_csv(index=False), model_source)
                st.success(f"Dataset 1 Columns: {selected_cols1}")
            with col2:
                selected_cols2 = get_important_columns(df2.to_csv(index=False), model_source)
                st.success(f"Dataset 2 Columns: {selected_cols2}")

            df1 = df1[selected_cols1] if selected_cols1 else df1
            df2 = df2[selected_cols2] if selected_cols2 else df2

            # === Comparison Visualization ===
            st.subheader("📈 Comparison Visualization")
            x_axis = st.selectbox("📌 Select X-Axis", df1.columns.tolist(), key="compare_x")
            y_axis = st.selectbox("📌 Select Y-Axis", df1.columns.tolist(), key="compare_y")
            layout = st.radio("🧩 Layout", ["Overlay", "Side-by-Side"], horizontal=True, key="compare_layout")
            chart_type = st.selectbox("📈 Chart Type", ["bar", "line", "scatter"], key="compare_chart")

            if x_axis and y_axis and x_axis in df1.columns and y_axis in df1.columns:
                fig = None
                if layout == "Overlay":
                    fig, explanation = visualize_comparison_overlay(df1, df2, x_axis, y_axis, "Dataset 1", "Dataset 2", chart_type)
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption(explanation)
                elif layout == "Side-by-Side":
                    fig1, fig2 = visualize_comparison_side_by_side(df1, df2, x_axis, y_axis, chart_type)
                    col1, col2 = st.columns(2)
                    if fig1:
                        col1.plotly_chart(fig1, use_container_width=True)
                    if fig2:
                        col2.plotly_chart(fig2, use_container_width=True)

            # === LLM-Suggested Comparison Insights ===
            st.subheader("🧠 AI-Suggested Comparison Insights")
            try:
                compare_suggestions = generate_comparison_insights(df1, df2, model_source)

                # Ensure it's a list of dicts
                if isinstance(compare_suggestions, str):
                    import json
                    compare_suggestions = json.loads(compare_suggestions)

                suggestion_titles = [item["title"] for item in compare_suggestions]
                selected_title = st.selectbox("Choose a Comparison Insight", suggestion_titles)

                if st.button("Generate Insight", key="compare_generate_btn"):
                    selected_item = next((i for i in compare_suggestions if i["title"] == selected_title), None)
                    if selected_item:
                        st.markdown(f"### Insight: {selected_item['title']}")
                        st.markdown(selected_item["description"])

            except Exception as e:
                st.error(f"Comparison insights generation failed: {e}")

            # === Chat-Based Comparison ===
            st.subheader("💬 Chat About This Comparison")
            compare_prompt = st.chat_input("Ask a question about the comparison...")
            if compare_prompt:
                merged_df = pd.concat([df1.assign(dataset="Dataset 1"), df2.assign(dataset="Dataset 2")])
                result = safe_llm_call(handle_user_query_dynamic, compare_prompt, merged_df, model_source, default={"response": "No response."})
                st.session_state.compare_chat.append({"user": compare_prompt, "assistant": result})

            for msg in st.session_state.compare_chat[::-1]:
                with st.chat_message("user"):
                    st.markdown(msg["user"])
                with st.chat_message("assistant"):
                    st.markdown(msg["assistant"].get("response", msg["assistant"]))

        except Exception as e:
            st.error(f"Error processing files: {e}")

# === Section 3: Summary & Export ===
if section == "Summary & Export":
    st.header("📦 Summary & Export")

    insights = st.session_state.get("insights", "No insights generated yet.")
    chat_logs = st.session_state.get("chat_history", []) + st.session_state.get("compare_chat", [])

    # --- Insight Summary ---
    st.subheader("🧠 Insight Summary")
    if insights:
        st.markdown(insights)
    else:
        st.warning("No insights to display.")

    # --- Chat History ---
    if chat_logs:
        st.subheader("💬 Chat History")
        for msg in chat_logs[::-1]:
            with st.chat_message("user"):
                st.markdown(msg["user"])
            with st.chat_message("assistant"):
                st.markdown(msg["assistant"].get("response", msg["assistant"]))
    insights_summary = ""
    if st.session_state.insights:
        if isinstance(st.session_state.insights, dict) and "response" in st.session_state.insights:
            insights_summary = st.session_state.insights["response"]
        else:
            insights_summary = str(st.session_state.insights)

    all_chat_logs = st.session_state.chat_history + st.session_state.compare_chat

    # --- Export Buttons ---
    st.subheader("📁 Export Report")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Export PDF"):
            try:
                pdf_path = generate_pdf_report(insights_summary, all_chat_logs)
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name="summary.pdf")
            except Exception as e:
                st.error(f"Failed to export PDF: {e}")

    with col2:
        if st.button("📊 Export PPTX"):
            try:
                pptx_path = export_to_pptx(insights_summary, all_chat_logs)
                with open(pptx_path, "rb") as f:
                    st.download_button("Download PPTX", f, file_name="summary.pptx")
            except Exception as e:
                st.error(f"Failed to export PPTX: {e}")
