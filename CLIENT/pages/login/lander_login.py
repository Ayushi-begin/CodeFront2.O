"""
lander.py

Objective:
    Lander/Login page for AI Plant Health Scanner.
    User must log in with Google before accessing the app.

Input:
    None (button triggers redirect to Google login via backend).

Output:
    Redirects user to backend /auth/login for Google authentication.
"""

import streamlit as st

# ✅ Backend URL (adjust if different)
BACKEND_URL = "http://localhost:5000"

st.set_page_config(page_title="AI Plant Health Scanner", page_icon="🌿", layout="centered")

# 🌿 Header Section
st.markdown("""
    <h1 style='text-align: center; color: green;'>🌿 AI Plant Health Scanner</h1>
    <p style='text-align: center; font-size:18px;'>
        Detect plant diseases, get treatments, and care tips using AI.<br>
        Please log in to continue.
    </p>
""", unsafe_allow_html=True)

st.divider()

# 🧑‍💻 Login Button
st.markdown(
    f"""
    <div style='text-align: center; margin-top: 40px;'>
        <a href="{BACKEND_URL}/auth/login" target="_self">
            <button style='background-color: green; color: white; padding: 12px 30px;
                           border: none; border-radius: 10px; font-size:18px; cursor: pointer;'>
                🔑 Login with Google
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# 🚫 Guest mode disabled
st.warning("⚠️ Access is restricted. Please log in to continue.")
