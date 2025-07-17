import streamlit as st
from layout.sidebar import render_sidebar
from layout.upload_area import render_upload_area
from layout.tabs_single import render_single_tabs
from layout.tabs_comparison import render_comparison_tabs
from dotenv import load_dotenv
from auth import login, signup, logout ,view_users,view_logs
from tour import render_guided_tour


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

st.sidebar.title("Authentication")
auth_mode = st.sidebar.radio("Select Option", ["Login", "Signup"])

st.sidebar.success(f"👤 Logged in as {st.session_state.username} ({st.session_state.role})")

if not st.session_state.logged_in:
    if auth_mode == "Login":
        login()
    else:
        signup()
    st.stop()

for key, default in {
    "mode": "single",
    "dataset_sessions": {},
    "compare_sessions": {},
    "current_session": None,
    "current_compare": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

load_dotenv()
st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

navigation = st.sidebar.radio("📂 Navigation", ["Dashboard", "Guided Tour"])

if navigation == "Guided Tour":
    render_guided_tour()
    st.stop()


st.title("Dynamic Impact Tool")

render_sidebar()

render_upload_area()

if st.session_state["mode"] == "single":
    render_single_tabs()
elif st.session_state["mode"] == "comparison":
    render_comparison_tabs()

logout()
if st.session_state.role == "admin":
    with st.sidebar.expander("🛠 Admin Panel", expanded=False):
        from auth import view_users
        view_users()
    with st.sidebar.expander("📜 Audit Logs"):
        view_logs()

