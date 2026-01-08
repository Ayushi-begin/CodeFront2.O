"""
File: services/geocoding_service.py

Objective:
    Convert location name into geographic coordinates (latitude, longitude)
    using OpenCage Geocoding API.

Input:
    location_name (str): User-provided location (city, village, etc.)

Output:
    dict: {"lat": float, "lon": float, "city": str}
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

def get_coordinates(location_name: str):
    """Fetch latitude and longitude from a location name."""
    if not OPENCAGE_API_KEY:
        raise ValueError("OpenCage API key missing in .env")

    url = f"https://api.opencagedata.com/geocode/v1/json?q={location_name}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("results"):
        geometry = data["results"][0]["geometry"]
        components = data["results"][0]["components"]
        lat, lon = geometry["lat"], geometry["lng"]
        city = components.get("city") or components.get("town") or components.get("village") or location_name
        return {"lat": lat, "lon": lon, "city": city}

    return None
