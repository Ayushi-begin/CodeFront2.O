"""
File: routes/weather_routes.py

Objective:
    Handle both coordinate-based and location-name-based weather requests.
    Converts location name to coordinates when necessary and returns
    agricultural weather analysis and recommendations.

Examples:
    1️⃣ /api/weather?lat=28.6139&lon=77.2090
    2️⃣ /api/weather?location=Lucknow
"""

from flask import Blueprint, jsonify, request
from controllers.weather_controller import (
    analyze_weather_for_agriculture,
    analyze_weather_by_location,  # ✅ new function from weather_controller
)

weather_bp = Blueprint("weather_bp", __name__)

@weather_bp.route("/weather", methods=["GET"])
def get_weather():
    """
    Accepts either:
        - lat & lon (float)  → direct coordinate input
        - location (str)     → city name, converted via geocoding
    """
    location = request.args.get("location")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    try:
        # ✅ Case 1: User provides location name (e.g., Lucknow)
        if location:
            result = analyze_weather_by_location(location)
            if "error" in result:
                return jsonify(result), 400
            return jsonify(result)

        # ✅ Case 2: User provides coordinates
        elif lat is not None and lon is not None:
            result = analyze_weather_for_agriculture(lat, lon)
            return jsonify(result)

        # ❌ Case 3: No valid input
        else:
            return jsonify({
                "error": "Please provide either a 'location' name or 'lat' and 'lon' values."
            }), 400

    except Exception as e:
        print(f"[ERROR] Weather route error: {e}")
        return jsonify({"error": "Something went wrong while processing weather data."}), 500
