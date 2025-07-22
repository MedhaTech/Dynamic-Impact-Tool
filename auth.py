import streamlit as st
import bcrypt
import secrets
from datetime import datetime, timedelta
from db import get_connection
from utils.logger import log_event

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user["role"]

            log_event(username, "login")
            st.success(f"Welcome, {username}! You are logged in as {user['role']}.")
            st.rerun()  
        else:
            st.error("Invalid username or password.")

def signup():
    st.subheader("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Create Account"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            st.warning("Username already exists.")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, hashed_pw, "user"),
            )
            conn.commit()
            st.success("Account created! Please log in.")
            st.session_state.page = "login"
        cursor.close()
        conn.close()

def request_password_reset():
    st.subheader("Request Password Reset")
    username = st.text_input("Enter your username")

    if st.button("Generate Reset Token"):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            token = secrets.token_urlsafe(16)
            expiry = datetime.now() + timedelta(minutes=15)
            cursor.execute("UPDATE users SET reset_token=%s, token_expiry=%s WHERE username=%s", (token, expiry, username))
            conn.commit()
            st.success("Reset token generated! (Dev Mode: shown below)")
            st.code(token)
            log_event("Reset Token Generated", username)
        else:
            st.error("Username not found.")
        cursor.close()
        conn.close()

def confirm_password_reset():
    st.subheader("Confirm Password Reset")
    username = st.text_input("Username")
    token = st.text_input("Reset Token")
    new_password = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user:
            st.error("User not found.")
        elif user["reset_token"] != token:
            st.error("Invalid reset token.")
        elif user["token_expiry"] is None or datetime.now() > user["token_expiry"]:
            st.error("Token has expired.")
        else:
            new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            cursor.execute("UPDATE users SET password_hash=%s, reset_token=NULL, token_expiry=NULL WHERE username=%s", (new_hash, username))
            conn.commit()
            st.success("Password reset successful.")
            log_event("Password Reset Confirmed", username)
        cursor.close()
        conn.close()

def logout():
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.experimental_rerun()

def view_users():
    st.subheader("Registered Users")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if rows:
        st.table(rows)
    else:
        st.info("No users found.")

def view_logs():
    st.subheader("Activity Logs")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, action, timestamp FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()

    if logs:
        st.table(logs)
    else:
        st.info("No logs available.")

def log_event(action, username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (username, action, timestamp) VALUES (%s, %s, %s)",
            (username, action, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Failed to log event: {e}")
