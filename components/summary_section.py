import streamlit as st
from chains.summary_chain import generate_summary

def render_summary_tab():
    st.subheader("Dataset Summaries")

    # Dataset A
    if st.session_state.df1 is not None:
        st.markdown("### Summary of Dataset A")
        if st.button("Generate Summary for Dataset A"):
            try:
                cols = st.session_state.selected_cols_1 or st.session_state.df1.columns.tolist()
                rows = st.session_state.df1[cols].sample(min(5, len(st.session_state.df1))).to_dict(orient="records")
                summary = generate_summary(cols, rows)
                st.session_state.summary_output_1 = summary
            except Exception as e:
                st.error(f"Failed: {e}")

        if st.session_state.summary_output_1:
            st.markdown(st.session_state.summary_output_1)

    # Dataset B
    if st.session_state.df2 is not None:
        st.markdown("### Summary of Dataset B")
        if st.button("Generate Summary for Dataset B"):
            try:
                cols = st.session_state.selected_cols_2 or st.session_state.df2.columns.tolist()
                rows = st.session_state.df2[cols].sample(min(5, len(st.session_state.df2))).to_dict(orient="records")
                summary = generate_summary(cols, rows)
                st.session_state.summary_output_2 = summary
            except Exception as e:
                st.error(f"Failed: {e}")

        if st.session_state.summary_output_2:
            st.markdown(st.session_state.summary_output_2)
