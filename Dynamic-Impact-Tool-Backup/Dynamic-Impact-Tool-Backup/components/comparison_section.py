import streamlit as st
from chains.comparison_chain import compare_datasets
from utils.comparator import quick_dataframe_comparison
from utils.file_loader import load_data
from dotenv import load_dotenv

load_dotenv()


def render_comparison_tab():
    st.title("🆚 Compare Datasets")
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file1 = st.file_uploader("Upload Dataset A", type=["csv", "xlsx"], key="fileA")
        if uploaded_file1:
            st.session_state.df1 = load_data(uploaded_file1)
            st.success("✅ Dataset A loaded.")

    with col2:
        uploaded_file2 = st.file_uploader("Upload Dataset B", type=["csv", "xlsx"], key="fileB")
        if uploaded_file2:
            st.session_state.df2 = load_data(uploaded_file2)
            st.success("✅ Dataset B loaded.")

    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        cols1 = st.session_state.df1.columns.tolist()
        cols2 = st.session_state.df2.columns.tolist()
        common_cols = list(set(cols1).intersection(set(cols2)))

        if len(common_cols) < 4:
            st.warning("⚠️ At least 4 common columns are required for meaningful comparison.")
            return

        st.subheader("🤖 AI-Based Comparison")

        if st.button("🔍 Run AI Comparison"):
            try:
                rows1 = st.session_state.df1[common_cols].sample(min(5, len(st.session_state.df1))).to_dict(orient="records")
                rows2 = st.session_state.df2[common_cols].sample(min(5, len(st.session_state.df2))).to_dict(orient="records")
                comparison = compare_datasets(common_cols, common_cols, rows1, rows2)
                st.session_state.comparison_result = comparison
                st.success("✅ AI Comparison completed successfully.")
            except Exception as e:
                st.error(f"❌ Error during comparison: {e}")

        if st.session_state.get("comparison_result"):
            st.markdown("### 🧠 Comparison Result")
            st.markdown(st.session_state.comparison_result)

        st.subheader("📊 Structural Overview")
        overview = quick_dataframe_comparison(st.session_state.df1, st.session_state.df2)
        st.json(overview)

    else:
        st.info("📂 Please upload both datasets to begin comparison.")
