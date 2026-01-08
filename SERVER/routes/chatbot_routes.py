# backend/routes/chatbot_routes.py

from flask import Blueprint, request, jsonify
from controllers.chatbot_controller import handle_chatbot_query

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot_message():
    """
    POST endpoint to handle chatbot messages.

    Expects:
        JSON: { "message": "user message here" }

    Returns:
        JSON: { "reply": "Gemini chatbot response" }
    """
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message.strip():
        return jsonify({"error": "Message cannot be empty."}), 400

    response = handle_chatbot_query(user_message)
    return jsonify(response)
