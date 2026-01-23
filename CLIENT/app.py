import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Plant Health Scanner",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. IMPORTS
from pages import results
from pages import chatbot
from pages import history
from pages import weather 
from pages import landing
from pages import home 

# ==========================================================
# 2. APP MODE STATE
# ==========================================================
if "app_mode" not in st.session_state:
    st.session_state.app_mode = False

# ✅ ENABLE APP MODE FROM URL
query_params = st.query_params
if query_params.get("app") == "1":
    st.session_state.app_mode = True

# ==========================================================
# 3. NAVIGATION SETUP
# ==========================================================
PAGES = ["Home", "Results", "Landing", "Chatbot", "History", "Weather Insights"]

default_index = 2  # Default to "Landing" (Index 2) if no parameter is provided
if "nav" in query_params:
    requested_page = query_params["nav"]
    if requested_page in PAGES:
        default_index = PAGES.index(requested_page)

# ==========================================================
# 4. SIDEBAR NAVIGATION
# ==========================================================
# Show sidebar only if app_mode is True
if st.session_state.app_mode:
    menu = st.sidebar.radio(
        "📍 Navigation", 
        PAGES, 
        index=default_index
    )
else:
    menu = "Landing"

# ==========================================================
# 5. PAGE ROUTING
# ==========================================================
if menu == "Home": 
    home.render()

elif menu == "Results": 
    results.render()

elif menu == "Landing": 
    landing.render()

elif menu == "Chatbot":
    if hasattr(chatbot, 'render'):
        chatbot.render()
    else:
        st.title("🤖 Chatbot")
        st.write("Chatbot module loaded.")

elif menu == "History":
    history.render()

elif menu == "Weather Insights":
    weather.render()
