# backend/config/settings.py

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the project."""

    # Load keys and credentials
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    #For the login part
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")
    APP_HOST = os.getenv("APP_HOST", "http://localhost:5000")

    # App settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))

# Initialize global settings
settings = Settings()
