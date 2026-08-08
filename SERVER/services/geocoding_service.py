"""
File: services/geocoding_service.py

Objective:
    Convert location name into geographic coordinates (latitude, longitude)
    using OpenWeather Geocoding API.
"""

import requests
from config.settings import Settings

def get_coordinates(location_name: str):
    """Fetch latitude and longitude from a location name."""
    api_key = Settings.OPENWEATHER_API_KEY
    if not api_key:
        raise ValueError("OpenWeather API key missing in config")

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            city = data[0].get("name", location_name)
            return {"lat": lat, "lon": lon, "city": city}

    return None
