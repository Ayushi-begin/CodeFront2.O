import streamlit as st
import requests

# ==========================================================
# 🔗 Backend Chatbot Endpoint
# ==========================================================
BASE_URL = "https://ai-plant-health-scanner.onrender.com/chatbot"

# ==========================================================
# 🧠 Bot API Call
# ==========================================================
def get_bot_response(user_message):
    try:
        payload = {"message": user_message}
        response = requests.post(BASE_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("reply", "Sorry, I didn't get that.")
        else:
            return f"⚠️ Error: {response.text}"
    except Exception as e:
        return f"❌ Failed to connect to chatbot API: {e}"

# ==========================================================
# ✅ MAIN RENDER FUNCTION (IMPORTANT)
# ==========================================================
def render():
    st.markdown(
        """
        <h2 style='color:#2E7D32; text-align:center;'>🤖 AI Plant Health Chatbot</h2>
        <p style='text-align:center;'>Ask anything about plant diseases, treatments, fertilizers, or care tips!</p>
        """,
        unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def handle_send():
        user_input = st.session_state.user_input.strip()
        if not user_input:
            return

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        bot_reply = get_bot_response(user_input)

        st.session_state.chat_history.append(
            {"role": "bot", "content": bot_reply}
        )

        st.session_state.user_input = ""

    st.markdown("---")
    st.subheader("🌻 Chat with Plant Expert (GREENY)")

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"🐨 **ME:** {chat['content']}")
        else:
            st.markdown(f"🌻 **GREENY:** {chat['content']}")

    st.text_input(
        "Type your message here...",
        key="user_input",
        on_change=handle_send
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
