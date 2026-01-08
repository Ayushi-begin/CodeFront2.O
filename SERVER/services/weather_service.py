# services/weather_service.py
import os
import requests
from config.settings import Settings

BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(lat: float, lon: float):
    """
    Fetch current weather data from OpenWeather's free API.
    """
    api_key =Settings.OPENWEATHER_API_KEY
    if not api_key:
        raise ValueError("Weather API key is missing!")

    url = f"{BASE_URL}/weather"
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": api_key}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    current = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].capitalize(),
        "wind_speed": data["wind"]["speed"],
        "city": data["name"]
    }

    return current


def get_forecast_weather(lat: float, lon: float):
    """
    Fetch 5-day forecast data (every 3 hours) from OpenWeather's free API.
    We'll summarize it into daily averages for AI readiness.
    """
    api_key = Settings.OPENWEATHER_API_KEY
    if not api_key:
        raise ValueError("Weather API key is missing!")

    url = f"{BASE_URL}/forecast"
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": api_key}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Summarize into daily forecasts
    forecast_summary = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        condition = item["weather"][0]["description"]

        if date not in forecast_summary:
            forecast_summary[date] = {"temps": [], "conditions": []}

        forecast_summary[date]["temps"].append(temp)
        forecast_summary[date]["conditions"].append(condition)

    # Convert into list of daily summaries
    daily_forecast = []
    for date, values in forecast_summary.items():
        avg_temp = round(sum(values["temps"]) / len(values["temps"]), 1)
        common_condition = max(set(values["conditions"]), key=values["conditions"].count)
        daily_forecast.append({
            "date": date,
            "avg_temperature": avg_temp,
            "condition": common_condition.capitalize()
        })

    return daily_forecast[:3]  # next 3 days only
