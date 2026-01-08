# ==========================================================
# FILE: frontend/components/sidebar.py 
# ==========================================================

import streamlit as st
import os

def render_sidebar():
    """Render the green-themed navigation sidebar (WITHOUT login/logout)."""
    # ------------------------------------------------------
    # Correct absolute path to logo.png
    # ------------------------------------------------------
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    logo_path = os.path.join(project_root, "CLIENT", "assets", "logo.png")
    logo_path = os.path.abspath(logo_path)

    # Display the logo
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.error("❌ Logo not found. Expected at: " + logo_path)

    st.markdown("---")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Branding Section ---
    st.markdown("""
        <div style='padding:10px; border-radius:8px;
                    background: linear-gradient(135deg, #A5D6A7 0%, #2E7D32 100%);'>
            <h2 style='margin:5px 0; color:white;'>AGENTIC AI</h2>
            <h5 style='margin:0; color:#E8F5E9;'>AI Powered Plant Health Scanner</h5>
        </div>
    """, unsafe_allow_html=True)
