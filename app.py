# import streamlit as st
# from layout.sidebar import render_sidebar
# from layout.upload_area import render_upload_area
# from layout.tabs_single import render_single_tabs
# from layout.tabs_comparison import render_comparison_tabs
# from dotenv import load_dotenv
# from auth import login, signup, view_users, view_logs
# from tour import render_guided_tour

# # Session defaults
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.username = ""
#     st.session_state.role = ""

# if not st.session_state.logged_in:
#     st.title("Authentication")
#     auth_mode = st.radio("Select Option", ["Login", "Signup"], horizontal=True)
#     if auth_mode == "Login":
#         login()
#     else:
#         signup()
#     st.stop()

# # Set up Streamlit app config
# load_dotenv()
# st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

# # Initialize additional session state
# for key, default in {
#     "mode": "single",
#     "dataset_sessions": {},
#     "compare_sessions": {},
#     "current_session": None,
#     "current_compare": None
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# # Sidebar navigation
# navigation = st.sidebar.radio("📂 Navigation", ["Dashboard", "Guided Tour"])

# # Show logged-in user info
# st.sidebar.success(f"👤 Logged in as {st.session_state.username} ({st.session_state.role})")

# # Admin tools
# if st.session_state.role == "admin":
#     with st.sidebar.expander("🛠 Admin Panel", expanded=False):
#         view_users()
#     with st.sidebar.expander("📜 Audit Logs"):
#         view_logs()

# # Guided tour
# if navigation == "Guided Tour":
#     render_guided_tour()
#     st.stop()

# # Main dashboard
# st.title("Dynamic Impact Tool")
# render_sidebar()
# render_upload_area()

# if st.session_state["mode"] == "single":
#     render_single_tabs()
# elif st.session_state["mode"] == "comparison":
#     render_comparison_tabs()


# with st.sidebar:
#     st.markdown("---")
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""
#         st.session_state.role = ""
#         st.success("You have been logged out.")
#         st.rerun()



import streamlit as st
from layout.sidebar import render_sidebar
from layout.upload_area import render_upload_area
from layout.tabs_single import render_single_tabs
from layout.tabs_comparison import render_comparison_tabs
from dotenv import load_dotenv
from auth import login, signup, view_users, view_logs
from tour import render_guided_tour

# Session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.title("Authentication")
    auth_mode = st.radio("Select Option", ["Login", "Signup"], horizontal=True)
    if auth_mode == "Login":
        login()
    else:
        signup()
    st.stop()

# Set up Streamlit app config
load_dotenv()
st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

# Initialize additional session state
for key, default in {
    "mode": "single",
    "dataset_sessions": {},
    "compare_sessions": {},
    "current_session": None,
    "current_compare": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sidebar navigation
if st.session_state.role == "admin":
    navigation = st.sidebar.radio("📂 Navigation", ["Dashboard", "Guided Tour", "Admin Panel", "Audit Logs"])
else:
    navigation = st.sidebar.radio("📂 Navigation", ["Dashboard", "Guided Tour"])

# Show logged-in user info
st.sidebar.success(f"👤 Logged in as {st.session_state.username} ({st.session_state.role})")

# Add custom scrollbar styling
st.markdown("""
<style>
/* Smooth scroll for containers */
div[data-testid="stVerticalBlock"] > div[style*="overflow"] {
    scrollbar-width: thin;
    scrollbar-color: #ccc #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# Guided Tour
if navigation == "Guided Tour":
    render_guided_tour()
    st.stop()

# Admin Panel
elif navigation == "Admin Panel" and st.session_state.role == "admin":
    st.title("🛠 Admin Panel")

    with st.container():
        st.markdown("""
       Registered Users
        """, unsafe_allow_html=True)

        view_users()

        st.markdown("</div>", unsafe_allow_html=True)

# Audit Logs
elif navigation == "Audit Logs" and st.session_state.role == "admin":
    st.title("📜 Audit Logs")

    with st.container():
        st.markdown("""
       Recent Activity
        """, unsafe_allow_html=True)

        view_logs()

        st.markdown("</div>", unsafe_allow_html=True)

# Main Dashboard
elif navigation == "Dashboard":
    st.title("Dynamic Impact Tool")
    render_sidebar()
    render_upload_area()

    if st.session_state["mode"] == "single":
        render_single_tabs()
    elif st.session_state["mode"] == "comparison":
        render_comparison_tabs()

# Optional: Logout
with st.sidebar:
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.success("You have been logged out.")
        st.rerun()