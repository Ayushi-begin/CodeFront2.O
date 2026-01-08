# ==========================================================
# FILE: frontend/pages/weather.py
# ==========================================================
"""
Objective:
    Allow user to enter a city name and fetch detailed weather info including:
    - Current weather
    - 3-day forecast
    - AI summary
    - Recommendation

Flow:
    - User inputs city name
    - Backend API returns detailed structure
    - Display weather + forecast + AI insights
"""

import streamlit as st
from utils import api_client


def render():
    st.title("⛅ Weather Insights")

    st.write("Enter a city name to get live weather details, forecast, and AI insights.")

    # ----------------------------------------------------------
    #  User Input: City Name
    # ----------------------------------------------------------
    city = st.text_input("🏙️ Enter City Name")

    if st.button("Get Weather"):
        if not city.strip():
            st.warning("⚠️ Please enter a valid city name.")
            return

        # ------------------------------------------------------
        # Fetch Weather Data From Backend
        # ------------------------------------------------------
        with st.spinner("Fetching weather data..."):
            weather_data = api_client.get_weather(city)

        if not weather_data:
            st.error("❌ Unable to fetch weather. Please check the city name.")
            return

        # ======================================================
        # ✅ Extract Data Properly From Backend Response
        # ======================================================

        current = weather_data.get("current_weather", {})
        forecast = weather_data.get("forecast", [])
        reco = weather_data.get("recommendation", "No recommendation available.")
        ai_summary = weather_data.get("ai_ready_context", {}).get("summary", "No summary.")

        location = weather_data.get("location", {})

        # ------------------------------------------------------
        # 3️⃣ Display Main Weather Info
        # ------------------------------------------------------
        st.subheader(f"🌤 Current Weather — {current.get('city', city).title()}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperature", f"{current.get('temperature', 'N/A')}°C")
        col2.metric("Humidity", f"{current.get('humidity', 'N/A')}%")
        col3.metric("Wind Speed", f"{current.get('wind_speed', 'N/A')} m/s")
        col4.metric("Condition", current.get("condition", "N/A"))

        # ------------------------------------------------------
        # 4️⃣ Display Forecast (Next 3 Days)
        # ------------------------------------------------------
        st.subheader("📅 3-Day Forecast")

        if forecast:
            for day in forecast:
                with st.container():
                    st.markdown(f"""
                    **📆 {day.get('date', 'N/A')}**  
                    🌡 Avg Temp: **{day.get('avg_temperature', 'N/A')}°C**  
                    🌥 Condition: **{day.get('condition', 'N/A')}**
                    """)
                    st.markdown("---")
        else:
            st.info("No forecast data available.")

        # ------------------------------------------------------
        # 5️⃣ AI Summary
        # ------------------------------------------------------
        st.subheader("🤖 AI Summary")
        st.success(ai_summary)

        # ------------------------------------------------------
        # 6️⃣ Recommendation
        # ------------------------------------------------------
        st.subheader("🌱 Recommendation")
        st.info(reco)

        # ------------------------------------------------------
        # 7️⃣ Location Info
        # ------------------------------------------------------
        st.subheader("📍 Location Details")
        st.write(f"Latitude: **{location.get('lat', 'N/A')}**")
        st.write(f"Longitude: **{location.get('lon', 'N/A')}**")


# Manual Test Run
if __name__ == "__main__":
    render()
