import streamlit as st
from chains.visual_chain import generate_visual_suggestions
from utils.visualizer import render_chart

def render_visualizations_tab():
    st.subheader("📊 Visual Insights")

    # Dataset picker
    dataset_choice = st.radio("Choose Dataset", ["Dataset A", "Dataset B"], horizontal=True)
    df_key = "df1" if dataset_choice == "Dataset A" else "df2"
    vis_key = "visual_suggestions_1" if df_key == "df1" else "visual_suggestions_2"

    df = st.session_state.get(df_key)
    if df is None:
        st.warning(f"{dataset_choice} not loaded.")
        return

    # Only show the suggestion logic AFTER user clicks
    show_suggestions = False

    if st.button("🔁 Generate Visualization Suggestions"):
        suggestions = generate_visual_suggestions(df)
        st.session_state[vis_key] = suggestions
        st.success("Suggestions generated!")
        show_suggestions = True  # flag to show rest of UI

        # Debugging: show raw LLM output
        if "last_llm_visual_raw" in st.session_state:
            with st.expander("🧠 Raw LLM Output from Groq"):
                st.code(st.session_state["last_llm_visual_raw"], language="python")

    # ✅ Only try to render dropdown *if* we have valid suggestions
    suggestions = st.session_state.get(vis_key, [])

    if suggestions:
        valid_suggestions = [s for s in suggestions if s.get("chart")]
        if valid_suggestions:
            labels = [
                f"{s['chart']['type'].title()} — {s['chart']['x']} vs {s['chart'].get('y', '')}"
                for s in valid_suggestions
            ]

            selected = st.selectbox("Select a visualization", labels, index=0)
            selected_chart = valid_suggestions[labels.index(selected)]

            if st.button("📈 Generate Chart"):
                st.markdown(f"**🧠 Insight:** {selected_chart['insight']}")
                chart = selected_chart["chart"]

                # Check column validity
                missing_cols = []
                if chart["x"] not in df.columns:
                    missing_cols.append(chart["x"])
                if chart.get("y") and chart["y"] not in df.columns:
                    missing_cols.append(chart["y"])
                if missing_cols:
                    st.error(f"⚠️ Column(s) not found in dataset: {', '.join(missing_cols)}")
                    return

                try:
                    fig = render_chart(df, chart_type=chart["type"], x=chart["x"], y=chart.get("y"))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Chart rendering failed: {e}")
        else:
            if show_suggestions:  # only show this if user clicked generate
                st.warning("No valid visualizations available. Try generating suggestions again.")
