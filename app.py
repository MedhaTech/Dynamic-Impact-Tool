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



# import streamlit as st
# from layout.sidebar import render_sidebar
# from layout.upload_area import render_upload_area
# from layout.tabs_single import render_single_tabs
# from layout.tabs_comparison import render_comparison_tabs
# from dotenv import load_dotenv
# from auth import login, signup, view_users, view_logs
# from tour import render_guided_tour

# load_dotenv()
# st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

# # 🔐 Authentication check
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

# # 🟡 Show Guided Tour once after login
# if "has_seen_tour" not in st.session_state:
#     st.session_state.has_seen_tour = False

# if not st.session_state.has_seen_tour:
#     st.session_state.has_seen_tour = True
#     st.query_params.update(page="Guided Tour")  # ✅ Capitalized to match nav options
#     render_guided_tour()
#     st.stop()

# # 🧠 Initialize main session state variables
# for key, default in {
#     "mode": "single",
#     "dataset_sessions": {},
#     "compare_sessions": {},
#     "current_session": None,
#     "current_compare": None
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# # ⬅️ Page Routing
# page = st.query_params.get("page", ["Dashboard"])[0].title()  # Default to Dashboard, title-case it

# # 🎛 Sidebar Navigation
# if st.session_state.role == "admin":
#     nav_options = ["Dashboard", "Guided Tour", "Admin Panel", "Audit Logs"]
# else:
#     nav_options = ["Dashboard", "Guided Tour"]

# # 🛡 Safe index lookup
# try:
#     nav_index = nav_options.index(page)
# except ValueError:
#     nav_index = 0  # Fallback to first item

# navigation = st.sidebar.radio("📂 Navigation", nav_options, index=nav_index)

# st.sidebar.success(f"👤 Logged in as {st.session_state.username} ({st.session_state.role})")

# # 🌐 Optional scrollbar theme
# st.markdown("""
# <style>
# div[data-testid="stVerticalBlock"] > div[style*="overflow"] {
#     scrollbar-width: thin;
#     scrollbar-color: #ccc #f9f9f9;
# }
# </style>
# """, unsafe_allow_html=True)

# # 🚀 Guided Tour Page
# if navigation == "Guided Tour":
#     render_guided_tour()
#     st.stop()

# # 🛠 Admin Panel
# if navigation == "Admin Panel" and st.session_state.role == "admin":
#     st.title("🛠 Admin Panel")
#     view_users()

# # 📜 Audit Logs
# elif navigation == "Audit Logs" and st.session_state.role == "admin":
#     st.title("📜 Audit Logs")
#     view_logs()

# # 📊 Dashboard Page
# elif navigation == "Dashboard":
#     st.title("Dynamic Impact Tool")
#     render_sidebar()
#     render_upload_area()

#     if st.session_state["mode"] == "single":
#         render_single_tabs()
#     elif st.session_state["mode"] == "comparison":
#         render_comparison_tabs()

# # 🔓 Logout Button
# with st.sidebar:
#     st.markdown("---")
#     if st.button("Logout"):
#         st.session_state.clear()
#         st.success("You have been logged out.")
#         st.rerun()


def inject_auth_css():
    st.markdown("""
        <style>
        html, body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            font-family: 'Segoe UI', sans-serif;
        }

        .stApp {
            background: transparent;
        }

        .bg-container {
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            z-index: -1;
        }

        .bg-container img {
            object-fit: cover;
            width: 100%;
            height: 100%;
            opacity: 0.25;
            filter: blur(6px) brightness(1.1);
        }

        .auth-box {
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            max-width: 400px;
            margin: 8vh auto;
        }

        @media screen and (max-width: 600px) {
            .auth-box {
                width: 90% !important;
                padding: 1.5rem;
                margin: 5vh auto;
                border-radius: 12px;
            }

            .auth-title {
                font-size: 1.4rem !important;
            }

            .stTextInput > div > input {
                font-size: 16px !important;
            }

            button[kind="primary"] {
                font-size: 16px !important;
                padding: 0.6rem 1.2rem !important;
            }
        }

        .auth-title {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 1.2rem;
            font-weight: 700;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="bg-container">
            <img src="https://images.unsplash.com/photo-1503264116251-35a269479413?auto=format&fit=crop&w=1950&q=80" />
        </div>
    """, unsafe_allow_html=True)


import streamlit as st
from layout.sidebar import render_sidebar
from layout.upload_area import render_upload_area
from layout.tabs_single import render_single_tabs
from layout.tabs_comparison import render_comparison_tabs
from dotenv import load_dotenv
from auth import login, signup, view_users, view_logs
from tour import render_guided_tour
from utils.groq_handler import call_groq_model, call_ollama_model
from utils.logger import logger

import json
import traceback
import ast

load_dotenv()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.title("Authentication")
    auth_mode = st.radio("Select Option", ["Login", "Signup"], horizontal=True)
    if auth_mode == "Login":
        inject_auth_css()
        login()
    else:
        signup()
        inject_auth_css()
    st.stop()


st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

if "has_seen_tour" not in st.session_state:
    st.session_state.has_seen_tour = False

if not st.session_state.has_seen_tour:
    st.session_state.has_seen_tour = True
    st.query_params.update(page="Guided Tour")
    render_guided_tour()
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

page = st.query_params.get("page", ["Dashboard"])[0].title()

if st.session_state.role == "admin":
    nav_options = ["Dashboard", "Guided Tour", "Admin Panel", "Audit Logs"]
else:
    nav_options = ["Dashboard", "Guided Tour"]

try:
    nav_index = nav_options.index(page)
except ValueError:
    nav_index = 0

navigation = st.sidebar.radio("Navigation", nav_options, index=nav_index)

st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")

st.markdown("""
<style>
div[data-testid="stVerticalBlock"] > div[style*="overflow"] {
    scrollbar-width: thin;
    scrollbar-color: #ccc #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

if navigation == "Guided Tour":
    render_guided_tour()
    st.stop()

# 🛠 Admin Panel
if navigation == "Admin Panel" and st.session_state.role == "admin":
    st.title("Admin Panel")
    view_users()

# \ud83d\udcdc Audit Logs
elif navigation == "Audit Logs" and st.session_state.role == "admin":
    st.title("Audit Logs")
    view_logs()

# \ud83d\udcca Dashboard Page
elif navigation == "Dashboard":
    st.title("Dynamic Impact Tool")
    render_sidebar()
    render_upload_area()

    if st.session_state["mode"] == "single":
        render_single_tabs()
    elif st.session_state["mode"] == "comparison":
        render_comparison_tabs()

# \ud83d\udd13 Logout Button
with st.sidebar:
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.rerun()

# 🔍 Optional: Add user query handling function here if needed elsewhere
