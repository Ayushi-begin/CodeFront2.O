# backend/services/gemini_service.py

import google.generativeai as genai
from config.settings import settings

class GeminiService:
    """Service layer for communicating with Gemini API."""

    def __init__(self):
        # Configure the Gemini SDK
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Load the Gemini 2.5 Flash model
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_response(self, user_query: str) -> str:
        """
        Sends a user message to Gemini and returns the model's response.
        
        Args:
            user_query (str): The text message from the user.

        Returns:
            str: Gemini-generated chatbot response.
        """
        try:
            response = self.model.generate_content(user_query)
            return response.text
        except Exception as e:
            print(f"[ERROR] Gemini API Error: {e}")
            return "Sorry, I'm having trouble connecting to the Gemini model right now."
