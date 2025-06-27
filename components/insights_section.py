import streamlit as st
from chains.category_chain import generate_insight_categories
from chains.insight_chain import generate_insights_for_category

def render_insights_tab():
    st.subheader("AI-Generated Insight Explorer")

    # Dataset A
    if st.session_state.df1 is not None:
        st.markdown("### Insights for Dataset A")

        if st.button("Generate Insight Categories (A)"):
            if "last_llm_insight_category_raw" in st.session_state:
                with st.expander("🧠 Raw LLM Category Output"):
                    st.code(st.session_state["last_llm_insight_category_raw"], language="python")

            try:
                cols = st.session_state.selected_cols_1 or st.session_state.df1.columns.tolist()
                rows = st.session_state.df1[cols].sample(min(5, len(st.session_state.df1))).to_dict(orient="records")
                categories = generate_insight_categories(cols, rows)
                st.session_state.insight_categories_1 = categories
            except Exception as e:
                st.error(f"Category generation failed: {e}")

        if st.session_state.insight_categories_1:
            selected = st.selectbox("Select Insight Category", st.session_state.insight_categories_1, key="insight_cat_1")
            st.session_state.selected_category_1 = selected

        if st.session_state.selected_category_1:
            if st.button("Generate Insights for Selected Category (A)"):
                try:
                    cols = st.session_state.selected_cols_1 or st.session_state.df1.columns.tolist()
                    rows = st.session_state.df1[cols].sample(min(5, len(st.session_state.df1))).to_dict(orient="records")
                    insights = generate_insights_for_category(cols, rows, st.session_state.selected_category_1)

                    st.session_state.category_insights_1[st.session_state.selected_category_1] = insights
                except Exception as e:
                    st.error(f"Insight generation failed: {e}")
            if not isinstance(st.session_state.get("category_insights_1"), dict):
                st.session_state.category_insights_1 = {}
            insights = st.session_state.category_insights_1.get(st.session_state.selected_category_1)
            if insights:
                st.markdown(insights)

    # Dataset B
    if st.session_state.df2 is not None:
        st.markdown("### Insights for Dataset B")

        if st.button("Generate Insight Categories (B)"):
            try:
                cols = st.session_state.selected_cols_2 or st.session_state.df2.columns.tolist()
                rows = st.session_state.df2[cols].sample(min(5, len(st.session_state.df2))).to_dict(orient="records")
                categories = generate_insight_categories(cols, rows)
                st.session_state.insight_categories_2 = categories
            except Exception as e:
                st.error(f"Category generation failed: {e}")

        if st.session_state.insight_categories_2:
            selected = st.selectbox("Select Insight Category", st.session_state.insight_categories_2, key="insight_cat_2")
            st.session_state.selected_category_2 = selected

        if st.session_state.selected_category_2:
            if st.button("Generate Insights for Selected Category (B)"):
                try:
                    cols = st.session_state.selected_cols_2 or st.session_state.df2.columns.tolist()
                    rows = st.session_state.df2[cols].sample(min(5, len(st.session_state.df2))).to_dict(orient="records")
                    insights = generate_insights_for_category(cols, rows, st.session_state.selected_category_2)
                    st.session_state.category_insights_2[st.session_state.selected_category_2] = insights
                except Exception as e:
                    st.error(f"Insight generation failed: {e}")
            if not isinstance(st.session_state.get("category_insights_2"), dict):
                st.session_state.category_insights_2 = {}
            insights = st.session_state.category_insights_2.get(st.session_state.selected_category_2)
            if insights:
                st.markdown(insights)

