import streamlit as st
import bcrypt
import json
import os
import pandas as pd
import datetime
import time
from html import escape

LOG_FILE = "logs.json"

def log_event(event, actor, target=None, details=""):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append({
        "timestamp": str(datetime.datetime.now()),
        "event": event,
        "actor": actor,
        "target": target,
        "details": details
    })
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

USER_FILE = "users.json"
import streamlit as st

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
            overflow: hidden;
        }

        .bg-container img {
            object-fit: cover;
            width: 100%;
            height: 100%;
            opacity: 0.25;
            filter: blur(4px) brightness(1.1);
        }

        .auth-box {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
            max-width: 420px;
            margin: 8vh auto;
        }

        .auth-title {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 1.2rem;
            font-weight: 700;
            color: #1a2b4c;
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
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="bg-container">
            <img src="https://img.freepik.com/premium-vector/serene-abstract-wave-background-with-calming-gradient-effect-great-ui-design_884160-1817.jpg" />
        </div>
    """, unsafe_allow_html=True)



def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup():
    inject_auth_css()
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="auth-title">📝 Sign Up</div>', unsafe_allow_html=True)

    users = load_users()
    new_user = st.text_input("👤 New Username", key="signup_username")
    new_pass = st.text_input("🔒 New Password", type="password", key="signup_password")
    role = st.selectbox("👥 Role", ["user", "admin"], key="signup_role")
    log_event("signup", new_user)

    if st.button("Create Account"):
        if new_user in users:
            st.error("Username already exists.")
        elif len(new_pass) < 4:
            st.warning("Password must be at least 4 characters.")
        else:
            users[new_user] = {
                "password": hash_password(new_pass),
                "role": role
            }
            save_users(users)
            st.success("Account created! You can now login.")
            st.toast("🎉 Signup successful!", icon="🎈")
            time.sleep(1.5)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def login():
    inject_auth_css()
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="auth-title">🔐 Login</div>', unsafe_allow_html=True)

    users = load_users()
    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔒 Password", type="password", key="login_password")
    log_event("login", username)

    if st.button("Login"):
        if username in users and check_password(password, users[username]["password"]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.balloons()
            st.toast("Logged in!", icon="🚀")
            st.success(f"Welcome back, {username}!", icon="🤖")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()


def reduce_sidebar_padding():
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .stSelectbox, .stButton, .stMarkdown {
            margin-bottom: 0.25rem;
        }
        </style>
    """, unsafe_allow_html=True)

def view_users():
    reduce_sidebar_padding()
    st.subheader("🧑‍💼 Manage Registered Users")
    users = load_users()

    for user, info in users.items():
        cols = st.columns([3, 2, 2, 1])
        with cols[0]:
            st.markdown(f"**👤 {user}**")
        with cols[1]:
            new_role = st.selectbox("Role", ["user", "admin"], index=["user", "admin"].index(info["role"]), key=f"role_{user}")
        with cols[2]:
            if new_role != info["role"]:
                # 🔥 Log the role change before updating
                log_event(
                    event="role_change",
                    actor=st.session_state.username,
                    target=user,
                    details=f"{info['role']} → {new_role}"
                )
                users[user]["role"] = new_role
                save_users(users)
                st.success(f"Updated role for `{user}` to `{new_role}`")
        with cols[3]:
            if st.button("🗑️", key=f"delete_{user}"):
                # 🔥 Log the user deletion before removing
                log_event(
                    event="delete_user",
                    actor=st.session_state.username,
                    target=user
                )
                del users[user]
                save_users(users)
                st.warning(f"Deleted user `{user}`")
                st.rerun()

    # CSV Export
    user_df = pd.DataFrame([
        {"Username": u, "Role": info["role"]} for u, info in users.items()
    ])
    csv = user_df.to_csv(index=False).encode('utf-8')
    st.download_button("📤 Export as CSV", data=csv, file_name="users.csv", mime='text/csv')


LOG_FILE = "audit_log.json"  # Update path if needed

def view_logs():
    st.subheader("📜 Audit Log")

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

        log_entries = ""
        for entry in reversed(logs[-50:]):  # Last 50 logs
            timestamp = escape(entry.get("timestamp", ""))
            event = escape(entry.get("event", ""))
            actor = escape(entry.get("actor", ""))
            target = escape(entry.get("target", "")) if entry.get("target") else ""
            details = escape(entry.get("details", "")) if entry.get("details") else ""

            log_entries += f"""
            <div style="
                background-color: rgba(255,255,255,0.05);
                border: 1px solid rgba(180, 180, 180, 0.2);
                padding: 10px 14px;
                margin-bottom: 10px;
                border-radius: 10px;
                font-size: 0.88rem;
                line-height: 1.5;
                color: var(--text-color);
            ">
                🕓 <code>{timestamp}</code><br>
                🔧 <strong>{event}</strong> by <code>{actor}</code><br>
                {'🎯 Target: <code>' + target + '</code><br>' if target else ''}
                {'📝 ' + details if details else ''}
            </div>
            """

        st.markdown(
            f"""
            <div style="max-height: 480px; overflow-y: auto; padding-right: 10px;">
                {log_entries}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.info("No logs yet.")