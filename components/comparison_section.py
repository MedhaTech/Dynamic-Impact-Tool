import streamlit as st
from chains.comparison_chain import compare_datasets
from utils.comparator import quick_dataframe_comparison

def render_comparison_tab():
    st.subheader("📊 Compare Dataset A vs Dataset B")

    if st.session_state.df1 is not None and st.session_state.df2 is not None:

        if st.button("Run AI Comparison"):
            try:
                cols1 = st.session_state.selected_cols_1 or st.session_state.df1.columns.tolist()
                cols2 = st.session_state.selected_cols_2 or st.session_state.df2.columns.tolist()

                rows1 = st.session_state.df1[cols1].sample(min(5, len(st.session_state.df1))).to_dict(orient="records")
                rows2 = st.session_state.df2[cols2].sample(min(5, len(st.session_state.df2))).to_dict(orient="records")

                comparison = compare_datasets(cols1, cols2, rows1, rows2)
                st.session_state.comparison_result = comparison

            except Exception as e:
                st.error(f"Comparison failed: {e}")

        if st.session_state.comparison_result:
            st.markdown(st.session_state.comparison_result)

        # Local logic (optional)
        st.markdown("### 🧮 Structural Comparison")
        local_comp = quick_dataframe_comparison(st.session_state.df1, st.session_state.df2)
        st.json(local_comp)

    else:
        st.warning("Please load both datasets to enable comparison.")


# import streamlit as st
# from utils.comparator import render_comparison_charts
# from chains.comparison_chain import generate_llm_diff_summary

# def render_comparison_tab():
#     st.subheader("🔁 Visual Comparison Between Datasets")

#     df1 = st.session_state.get("df1")
#     df2 = st.session_state.get("df2")

#     if df1 is None or df2 is None:
#         st.warning("Upload both Dataset A and B to enable comparison.")
#         return

#     common_cols = list(set(df1.columns).intersection(df2.columns))
#     if not common_cols:
#         st.error("No common columns found for comparison.")
#         return

#     col_to_compare = st.selectbox("🧠 Select a common column to compare:", common_cols)
#     chart_type = st.selectbox("📊 Chart type:", ["bar", "histogram", "box"])

#     if st.button("🔍 Generate Comparison Charts"):
#         render_comparison_charts(df1, df2, chart_type, col_to_compare)

#         with st.spinner("🧠 Asking AI to summarize differences..."):
#             diff = generate_llm_diff_summary(df1, df2, col_to_compare)
#             st.markdown("### 🧠 AI Summary of Differences")
#             st.markdown(diff)
