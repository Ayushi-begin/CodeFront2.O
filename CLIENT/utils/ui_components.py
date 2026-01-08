# ==========================================================
# FILE: frontend/utils/ui_components.py
# ==========================================================

import streamlit as st

def display_title(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.write(subtitle)

def display_center_button(label: str, key=None):
    col = st.columns([1, 1, 1])[1]
    return col.button(label, key=key, use_container_width=True, type="primary")
