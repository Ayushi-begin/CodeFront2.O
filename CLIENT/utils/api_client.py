# ==========================================================
# FILE: frontend/utils/api_client.py
# ==========================================================
"""
Objective:
    Provides reusable API functions for communicating with the Flask backend.

Functions:
    1. get_yolo_result(image_source): Upload image for YOLO disease detection
    2. get_weather(location): Fetch weather data from city/location name
    3. get_weather_by_coords(lat, lon): Fetch weather using lat/lon
    4. get_agentic_summary(lat, lon, disease, confidence): Get AI-generated advice
    5. save_to_history(data): Save analyzed result to backend user history
"""

import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# Base URL of Flask backend

BASE_URL = os.getenv("APP_HOST")


# ==========================================================
# 1️⃣ YOLO DISEASE DETECTION
# ==========================================================
def get_yolo_result(image_source):
    """
    Upload image to backend for YOLO-based plant disease detection.
    Input:
        image_source (BytesIO): Uploaded/captured image
    Output:
        dict: Detection info { disease, confidence, annotated_image }
    """
    try:
        # Correctly send as a file with filename and type
        files = {"image": ("uploaded_image.jpg", image_source, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
        if response.ok:
            return response.json()
        st.error(f"❌ YOLO API Error: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Connection error with YOLO API: {e}")
    return None


# ==========================================================
# 2️⃣ WEATHER FETCH USING LOCATION
# ==========================================================
def get_weather(location: str):
    """
    Fetch weather using only the location name.
    Backend expects: GET /api/weather?location=NAME
    """
    try:
        response = requests.get(
            f"{BASE_URL}/api/weather",
            params={"location": location}
        )

        if response.ok:
            return response.json()

        st.error(f"⚠️ Weather API Error: {response.text}")

    except Exception as e:
        st.error(f"⚠️ Weather API connection failed: {e}")

    return None


# ==========================================================
# 3️⃣ WEATHER FETCH USING COORDINATES (Optional helper)
# ==========================================================
def get_weather_by_coords(lat, lon):
    """
    Fetch weather info when coordinates are already available.
    Input:
        lat (float), lon (float)
    Output:
        dict: Weather and recommendation data
    """
    try:
        response = requests.get(f"{BASE_URL}/api/weather", params={"lat": float(lat), "lon": float(lon)})
        if response.ok:
            return response.json()
        st.error(f"⚠️ Weather API (coords) Error: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Weather API connection failed: {e}")
    return None


# ==========================================================
# 4️⃣ AI RECOMMENDATION SUMMARY
# ==========================================================
def get_agentic_summary(lat, lon, disease, confidence):
    """
    Send disease and weather info to backend AI model to get summary and recommendation.
    """
    try:
        payload = {
            "lat": lat,
            "lon": lon,
            "disease": disease,
            "confidence": confidence,
        }
        response = requests.post(f"{BASE_URL}/api/agentic-ai", json=payload)
        if response.ok:
            return response.json()
        st.error(f"⚠️ AI Summary API Error: {response.text}")
    except Exception as e:
        st.error(f"⚠️ AI Summary connection failed: {e}")
    return None


# ==========================================================
# 5️⃣ SAVE RESULT TO HISTORY 
# ==========================================================
def save_history_to_backend(history_data):
    try:
        response = requests.post(
            f"{BASE_URL}/api/save-history", json=history_data
        )
        if response.ok:
            return True
    except:
        return False

def get_history():
    try:
        response = requests.get(f"{BASE_URL}/api/get-history")
        if response.ok:
            return response.json()
    except:
        return []

def delete_history(record_id):
    try:
        res = requests.delete(f"{BASE_URL}/api/delete-history", params={"id": record_id})
        return res.ok
    except:
        return False


def delete_all_history():
    try:
        res = requests.delete(f"{BASE_URL}/api/delete-all-history")
        return res.ok
    except:
        return False

