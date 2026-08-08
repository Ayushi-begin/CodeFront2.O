"""
login_callback.py

Objective:
    Handle Google OAuth callback from backend,
    store user info in Streamlit session state,
    and redirect user to main dashboard (chatbot, etc.).

Input:
    JSON data automatically sent from backend's /auth/callback route
    via browser redirect after Google login.

Output:
    Saves user info in st.session_state and redirects to dashboard.
"""

import os
import streamlit as st
import json

st.set_page_config(page_title="Login Callback", page_icon="🔄")

BACKEND_URL = os.getenv("APP_HOST", "http://localhost:5000")

st.write("🔄 Logging you in... please wait...")

# -------------------------------------------------------
# Streamlit runs inside a browser, so we can access the
# URL parameters passed from Flask via query string.
# -------------------------------------------------------

query_params = st.query_params

if "user_info" in query_params:
    # Backend could redirect with user_info encoded as JSON
    user_info_json = query_params["user_info"]
    try:
        user_info = json.loads(user_info_json)
    except Exception:
        user_info = {}

    if user_info:
        st.session_state["logged_in"] = True
        st.session_state["user_info"] = user_info
        st.success(f"✅ Welcome, {user_info.get('name', 'User')}!")
        st.switch_page("pages/chatbot.py")
    else:
        st.error("⚠️ Login failed. Invalid user data received.")
else:
    st.error("⚠️ No user info found. Please login again.")
    st.markdown(f"[🔑 Go to Login]({BACKEND_URL}/auth/login)")
