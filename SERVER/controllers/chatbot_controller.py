# backend/controllers/chatbot_controller.py

from services.gemini_service import GeminiService
from utils.response_utils import success_response, error_response

# Initialize the Gemini service
gemini_service = GeminiService()

def handle_chatbot_query(user_message: str):
    """
    Processes chatbot messages using the Gemini service.

    Args:
        user_message (str): Input text from frontend.

    Returns:
        dict: API response with success or error message.
    """
    try:
        # Generate chatbot reply from Gemini
        reply = gemini_service.generate_response(user_message)
        return success_response(message="Chatbot reply generated successfully.", data={"reply": reply})
    except Exception as e:
        return error_response(message=f"Failed to generate chatbot response: {e}")
