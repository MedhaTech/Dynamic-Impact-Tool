import streamlit as st
from state.session_manager import init_session_state
from components.sidebar import render_sidebar
from components.dataset_viewer import render_data_preview
from components.summary_section import render_summary_tab
from components.insights_section import render_insights_tab
from components.comparison_section import render_comparison_tab
from components.visualizations_section import render_visualizations_tab 

st.set_page_config(page_title="LLM Dataset Analyzer", layout="wide")
init_session_state()

render_sidebar()

# Main View
st.title("📊 Dynamic Dataset Analyzer")
selected_tab = st.session_state.get("selected_tab", "Summary")

if selected_tab == "Summary":
    render_summary_tab()
elif selected_tab == "Insights":
    render_insights_tab()
elif selected_tab == "Comparison":
    render_comparison_tab()
elif selected_tab == "Visualizations":
    render_visualizations_tab()
    
render_data_preview()
