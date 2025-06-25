import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()

from utils.file_loader import load_data
from utils.insight_generator import generate_insights
from utils.chat_handler import handle_user_query_dynamic
from utils.visualizer import visualize_from_llm_response
from utils.column_selector import get_important_columns
from utils.insight_suggester import suggest_insight_options_explained, DEFAULT_INSIGHTS

st.set_page_config(page_title="LLM Powered Insight Generator", layout="wide")

with st.sidebar:
    st.markdown("<h1 style='font-size: 26px;'>Know Your Data</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV / Excel / JSON", type=['.csv', '.xlsx', '.json'])
    model_source = "groq"
    st.info(f"Using Model Backend: {model_source.upper()}")

if "insights" not in st.session_state:
    st.session_state.insights = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<h1 style='font-size: 30px;'>AI Input Configuration</h1>", unsafe_allow_html=True)

if uploaded_file:
    try:
        df = load_data(uploaded_file)
        st.success("File Loaded Successfully")
        st.markdown("<h2 style='font-size: 24px;'>Data Preview</h2>", unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        st.stop()

    st.markdown("<h2 style='font-size: 22px;'>Column Selection</h2>", unsafe_allow_html=True)
    selected_columns = st.multiselect(
        "Select columns for analysis (if none selected, all will be used):",
        options=df.columns.tolist(),
        default=df.columns.tolist()
    )
    df_selected = df[selected_columns]

    st.markdown("<h2 style='font-size: 22px;'>✨ AI-Selected Important Columns</h2>", unsafe_allow_html=True)
    selected_cols = get_important_columns(df_selected.to_csv(index=False), model_source=model_source)

    if len(selected_cols) < len(df_selected.columns):
        st.success(f"AI prioritized {len(selected_cols)} important columns: {selected_cols}")
        if set(['streams', 'in_spotify_playlists', 'in_apple_playlists', 'in_spotify_charts', 'in_apple_charts']).intersection(set(selected_cols)):
            st.markdown("""
These features are key indicators of **track performance** and **audience reach** across platforms. 
The AI uses them to analyze trends, popularity spikes, and streaming behavior.
""")
    else:
        st.warning("AI failed to prioritize columns, so showing all available columns.")

    if selected_cols:
        try:
            selected_df = df[selected_cols].head()
            st.dataframe(selected_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying selected columns: {e}")

    st.markdown("<h2 style='font-size: 22px;'>AI-Suggested Insights</h2>", unsafe_allow_html=True)
    suggested_insights = suggest_insight_options_explained(df_selected.to_csv(index=False), model_source=model_source)

    if suggested_insights:
        display_options = [f"{item['title']} - {item['description']}" for item in suggested_insights]
        selected_display = st.selectbox("Choose an Insight to Generate", display_options)
        selected_title = next((item['title'] for item in suggested_insights if item['title'] in selected_display), None)

        if st.button("Generate Selected Insight") and selected_title:
            with st.spinner("Generating insight..."):
                insight = generate_insights(df_selected, selected_title, model_source=model_source)
                st.session_state.insights = insight

        if st.session_state.insights:
            st.markdown("<h3 style='font-size: 20px;'>Insight</h3>", unsafe_allow_html=True)
            st.markdown(st.session_state.insights)
    else:
        st.warning("AI couldn't generate insight suggestions. Showing default options.")
        default_options = [f"{item['title']} - {item['description']}" for item in DEFAULT_INSIGHTS]
        selected_display = st.selectbox("Choose a Default Insight", default_options)
        selected_title = next((item['title'] for item in DEFAULT_INSIGHTS if item['title'] in selected_display), None)

        if st.button("Generate Default Insight") and selected_title:
            with st.spinner("Generating insight..."):
                insight = generate_insights(df_selected, selected_title, model_source=model_source)
                st.session_state.insights = insight

        if st.session_state.insights:
            st.markdown("<h3 style='font-size: 20px;'>Insight</h3>", unsafe_allow_html=True)
            st.markdown(st.session_state.insights)

    st.markdown("<h2 style='font-size: 22px;'>Talk to your Data</h2>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(msg["user"])

        with st.chat_message("assistant"):
            if isinstance(msg["assistant"], dict) and "chart_type" in msg["assistant"]:
                fig = visualize_from_llm_response(df_selected, msg["user"], msg["assistant"])
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Chart generation failed.")
            else:
                st.markdown(msg["assistant"])

            if msg.get("follow_ups"):
                for i, q in enumerate(msg["follow_ups"]):
                    st.button(f" {q}", key=f"history_followup_{i}_{msg['timestamp']}", on_click=lambda q=q: st.session_state.update({"chat_input": q}))

    user_input = st.chat_input("Type your message...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                result = handle_user_query_dynamic(user_input, df_selected, model_source=model_source)
                response = result["response"]
                follow_ups = result.get("follow_ups", [])

                st.session_state.chat_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "assistant": response,
                    "model": model_source,
                    "follow_ups": follow_ups
                })

                if isinstance(response, dict) and "chart_type" in response:
                    fig = visualize_from_llm_response(df_selected, user_input, response)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Chart generation failed.")
                else:
                    st.markdown(response)

                if follow_ups:
                    st.markdown("** Follow-up Suggestions:**")
                    for i, q in enumerate(follow_ups):
                        st.button(f"{q}", key=f"followup_{i}_{datetime.now().timestamp()}", on_click=lambda q=q: st.session_state.update({"chat_input": q}))

            except Exception as e:
                st.error(f"Agent failed: {e}")

    os.makedirs("chat_logs", exist_ok=True)
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### Download Your Chat")

        full_chat = "\n\n".join([
            f"[{entry['timestamp']}] You: {entry['user']}\n🤖 ({entry['model']}): {entry['assistant']}"
            for entry in st.session_state.chat_history
        ])

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_logs/{timestamp}_chat.txt"
        with open(filename, "w") as f:
            f.write(full_chat)

        with open(filename, "rb") as f:
            st.download_button("Download Chat Log", f, file_name=os.path.basename(filename), mime="text/plain")
