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
