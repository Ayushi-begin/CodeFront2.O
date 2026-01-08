# controllers/weather_controller.py
from services.weather_service import get_current_weather, get_forecast_weather
from services.geocoding_service import get_coordinates 


def analyze_weather_for_agriculture(lat: float, lon: float):
    """
    Combines current and forecast weather, generates simple
    agricultural recommendations (future: Agentic AI reasoning).
    """
    current = get_current_weather(lat, lon)
    forecast = get_forecast_weather(lat, lon)

    temp = current["temperature"]
    condition = current["condition"].lower()

    # Rule-based logic (AI reasoning layer will replace this later)
    if "rain" in condition:
        recommendation = "🌧️ Avoid planting — heavy rain detected today."
    elif temp < 15:
        recommendation = "❄️ Too cold for germination. Delay plantation."
    elif temp > 35:
        recommendation = "🔥 Hot weather — irrigation required if planting now."
    else:
        recommendation = "🌱 Good time to plant — favorable conditions detected."

    # Forecast reasoning
    for day in forecast:
        if "rain" in day["condition"].lower():
            recommendation += f" ⚠️ Rain expected on {day['date']} — plan irrigation accordingly."
            break
        elif day["avg_temperature"] < 15:
            recommendation += f" ⚠️ Temperature drop expected on {day['date']}."
            break

    return {
        "location": {"lat": lat, "lon": lon, "city": current.get("city")},
        "current_weather": current,
        "forecast": forecast,
        "recommendation": recommendation,
        "ai_ready_context": {
            "task": "agricultural weather analysis",
            "summary": f"Currently {condition} at {temp}°C. Upcoming forecast: {forecast[0]['condition']}.",
            "data": {
                "current": current,
                "forecast": forecast
            }
        }
    }


#for the geocoding
def analyze_weather_by_location(location_name: str):
    """
    Wrapper function: accepts a city/location name,
    converts it to coordinates, and calls analyze_weather_for_agriculture().
    """
    coords = get_coordinates(location_name)
    if not coords:
        return {"error": "Invalid location name or unable to get coordinates."}

    lat, lon = coords["lat"], coords["lon"]
    analysis = analyze_weather_for_agriculture(lat, lon)
    analysis["location"]["city"] = coords["city"]  # ensure correct city name
    return analysis