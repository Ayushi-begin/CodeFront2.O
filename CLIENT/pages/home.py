# ==========================================================
# FILE: frontend/pages/home.py
# ==========================================================
"""
Objective:
    Main interface for uploading or capturing plant leaf images,
    performing YOLO-based disease detection, fetching weather data,
    and getting AI-generated recommendations.

Flow:
    SCAN → Choose Input Method → YOLO Detection → Weather → AI Summary
"""

import streamlit as st
from utils import api_client
import requests

# ==========================================================
# FUNCTION: RENDER HOME PAGE
# ==========================================================
def render():
    """Render the Home Page for plant disease detection."""
    
    st.title("🌿 AI Powered Plant Health Scanner")
    st.write("Welcome! Click **SCAN** to analyze a plant leaf and get weather-based advice.")

    # ------------------------------------------------------
    # STEP 1: Initialize session state
    # ------------------------------------------------------
    if "scan_mode" not in st.session_state:
        st.session_state["scan_mode"] = None

    # ------------------------------------------------------
    # STEP 2: SCAN button
    # ------------------------------------------------------
    st.markdown("---")
    center = st.columns([1, 1, 1])
    with center[1]:
        if st.button("SCAN", width="stretch", type="primary"):  # ✅ updated
            st.session_state["scan_mode"] = "select_mode"

    # ------------------------------------------------------
    # STEP 3: Choose input method after clicking SCAN
    # ------------------------------------------------------
    if st.session_state["scan_mode"] == "select_mode":
        st.markdown("---")
        st.subheader("🔍 Select Input Method")

        input_method = st.radio(
            "Choose how to provide the image:",
            ["Use Camera", "Browse Files"],
            index=None,
            horizontal=True
        )

        # =============== CAMERA OPTION ===============
        if input_method == "Use Camera":
            camera_image = st.camera_input("📷 Capture a photo of the plant leaf")
            if camera_image:
                if st.button("🔍 Analyze Captured Image", type="primary"):
                    st.session_state["image_source"] = camera_image
                    st.session_state["scan_mode"] = "process"


        # =============== FILE UPLOAD OPTION ===============
        elif input_method == "Browse Files":
            uploaded_image = st.file_uploader("📁 Upload a leaf image", type=["jpg", "jpeg", "png"])
            if uploaded_image:
                if st.button("🔍 Analyze Uploaded Image", type="primary"):
                    st.session_state["image_source"] = uploaded_image
                    st.session_state["scan_mode"] = "process"
       
    # ------------------------------------------------------
    # RUN PROCESS IMAGE IF WE ARE IN PROCESS MODE
    # ------------------------------------------------------
    if st.session_state["scan_mode"] == "process":
        process_image(st.session_state["image_source"])


# ==========================================================
# FUNCTION: PROCESS IMAGE
# ==========================================================
def process_image(image_source):
    """Handles detection, weather fetch, and AI recommendation pipeline."""

    # STEP 1: Show preview
    st.markdown("### 📸 Image Preview and Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_source, caption="Uploaded Image", width="stretch")  # ✅ updated

    # STEP 2: YOLO Detection
    with st.spinner("🔍 Detecting plant disease using YOLO model..."):
        yolo_response = api_client.get_yolo_result(image_source)

    if not yolo_response or "detections" not in yolo_response:
        st.error("❌ Detection failed. Please try again.")
        return    

    # SAVE YOLO RESULT FOR RESULTS PAGE 🚀
    st.session_state["yolo_result"] = yolo_response 

    if not yolo_response or "detections" not in yolo_response:
        st.error("❌ Detection failed. Please try again.")
        return

    # Pick the highest-confidence detection
    top_detection = max(yolo_response["detections"], key=lambda x: x["confidence"])
    st.session_state["disease"] = top_detection["disease"]
    st.session_state["confidence"] = top_detection["confidence"]

    with col2:
        st.image(
            yolo_response.get("annotated_image"),
            caption="Analyzed Image (YOLO Output)",
            width="stretch"  # ✅ updated
        )

    st.success(
        f"✅ Detected Disease: **{top_detection['disease']}** "
        f"(Confidence: {top_detection['confidence']:.2f}%)"
    )

    # STEP 3: Get user location
    st.markdown("---")
    st.subheader("📍 Provide Your Location for Weather-Based Advice")

    user_location = st.text_input("Enter your location (e.g., Lucknow, Pune, Delhi):")

    if user_location:
        with st.spinner("🌦️ Fetching weather details..."):
            weather_response = api_client.get_weather(user_location)

        if weather_response:
            loc = weather_response.get("location", {})
            st.session_state["lat"] = loc.get("lat")
            st.session_state["lon"] = loc.get("lon")

            st.success("✅ Weather data fetched successfully!")
            st.json(weather_response.get("current_weather", {}))

            if weather_response.get("recommendation"):
                st.info(weather_response["recommendation"])

            # Proceed to AI summary
            generate_ai_summary()
            # ----------------------------------------------------------
            # SHOW AI SUMMARY ON HOME PAGE
            # ----------------------------------------------------------
            if "agentic_summary" in st.session_state:
                st.markdown("---")
                st.subheader("🤖 AI Summary & Recommendation")

                st.info(st.session_state["agentic_summary"])

                st.markdown("### 🌱 Full Recommendation")
                st.write(st.session_state["agentic_full"])

        else:
            st.error("⚠️ Failed to fetch weather data.")


# ==========================================================
# FUNCTION: GENERATE AI SUMMARY
# ==========================================================
def generate_ai_summary():
    """Fetches AI-based summary and recommendation."""
    if st.session_state.get("lat") and st.session_state.get("lon"):
        with st.spinner("🤖 Generating AI recommendation summary..."):
            ai_response = api_client.get_agentic_summary(
                lat=st.session_state["lat"],
                lon=st.session_state["lon"],
                disease=st.session_state["disease"],
                confidence=st.session_state["confidence"]
            )

        if ai_response:
            st.session_state["agentic_summary"] = ai_response.get("summary")
            st.session_state["agentic_full"] = ai_response.get("recommendation")

            st.success("🌱 AI Recommendation Ready!")

            # ❌ Removed redirect
            # st.session_state["scan_mode"] = None
            # st.session_state["page"] = "Results"

        else:
            st.error("⚠️ Failed to generate AI recommendation. Try again later.")
