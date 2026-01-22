"""
Objective:
    Main interface for uploading or capturing plant leaf images.
    FIX: Manually assigns image formats to prevent Streamlit 'AttributeError' crashes.
"""

import streamlit as st
import base64
import io
from PIL import Image
from utils import api_client

# ==========================================================
# 🛡️ HELPER: THE FORMAT ENFORCER
# ==========================================================
def load_and_fix_image(image_data):
    """
    Reads image data and manually sets the '.format' attribute.
    This prevents the 'AttributeError' in Streamlit Cloud.
    """
    try:
        image_obj = None

        # Case 1: UploadedFile or CameraInput
        if hasattr(image_data, "read"):
            image_data.seek(0)
            image_obj = Image.open(image_data)

        # Case 2: Raw Bytes (from Base64 decode)
        elif isinstance(image_data, bytes):
            image_obj = Image.open(io.BytesIO(image_data))
        
        # Case 3: Already a PIL Image
        elif isinstance(image_data, Image.Image):
            image_obj = image_data

        # 🚨 THE FIX: Force the format attribute
        if image_obj:
            if not getattr(image_obj, "format", None):
                image_obj.format = "JPEG"  # Fake it so Streamlit stops complaining
            return image_obj
            
        return None

    except Exception as e:
        print(f"Image Load Error: {e}")
        return None

# ==========================================================
# 🏠 MAIN RENDER FUNCTION
# ==========================================================
def render():
    st.title("🌿 AI Powered Plant Health Scanner")
    st.write("Welcome! Click **SCAN** to analyze a plant leaf.")

    if "scan_mode" not in st.session_state:
        st.session_state["scan_mode"] = None

    # --- SCAN BUTTON ---
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("SCAN", type="primary", use_container_width=True):
            st.session_state["scan_mode"] = "select_mode"

    # --- INPUT SELECTION ---
    if st.session_state["scan_mode"] == "select_mode":
        st.markdown("---")
        st.subheader("🔍 Select Input Method")
        input_method = st.radio("Choose source:", ["Use Camera", "Browse Files"], horizontal=True)

        if input_method == "Use Camera":
            camera_image = st.camera_input("📷 Capture photo")
            if camera_image:
                if st.button("🔍 Analyze Captured Image", type="primary"):
                    st.session_state["image_source"] = camera_image
                    st.session_state["scan_mode"] = "process"

        elif input_method == "Browse Files":
            uploaded_image = st.file_uploader("📁 Upload image", type=["jpg", "jpeg", "png"])
            if uploaded_image:
                if st.button("🔍 Analyze Uploaded Image", type="primary"):
                    st.session_state["image_source"] = uploaded_image
                    st.session_state["scan_mode"] = "process"
        
    # --- PROCESS TRIGGER ---
    if st.session_state["scan_mode"] == "process" and "image_source" in st.session_state:
        process_image(st.session_state["image_source"])

# ==========================================================
# ⚙️ PROCESS LOGIC
# ==========================================================
def process_image(image_source):
    st.markdown("### 📸 Image Preview and Analysis")
    col1, col2 = st.columns(2)

    # --- 1. DISPLAY UPLOADED IMAGE (Fixed) ---
    with col1:
        fixed_upload = load_and_fix_image(image_source)
        if fixed_upload:
            st.image(fixed_upload, caption="Uploaded Image", use_container_width=True)
        else:
            st.error("Could not load uploaded image.")

    # --- 2. RUN BACKEND API ---
    with st.spinner("🔍 Detecting plant disease..."):
        # Reset pointer for API
        if hasattr(image_source, "seek"):
            image_source.seek(0)
            
        yolo_response = api_client.get_yolo_result(image_source)

    if not yolo_response or "detections" not in yolo_response:
        st.error("❌ Detection failed. Server returned no data.")
        return    

    # Store results
    st.session_state["yolo_result"] = yolo_response 
    
    if yolo_response["detections"]:
        top_det = max(yolo_response["detections"], key=lambda x: x["confidence"])
        st.session_state["disease"] = top_det["disease"]
        st.session_state["confidence"] = top_det["confidence"]
        st.success(f"✅ Detected: **{top_det['disease']}** ({top_det['confidence']:.2f}%)")
    else:
        st.warning("No disease detected.")
        st.session_state["disease"] = "Healthy"
        st.session_state["confidence"] = 0.0

    # --- 3. DISPLAY ANNOTATED IMAGE (Fixed) ---
    with col2:
        annotated_b64 = yolo_response.get("annotated_image")
        
        if annotated_b64:
            try:
                # Clean Base64 string
                if "," in annotated_b64:
                    annotated_b64 = annotated_b64.split(",")[1]
                
                # Decode -> Bytes -> Fixed Image
                img_bytes = base64.b64decode(annotated_b64)
                fixed_annotated = load_and_fix_image(img_bytes)
                
                if fixed_annotated:
                    st.image(fixed_annotated, caption="Analyzed Image", use_container_width=True)
                else:
                    st.error("Failed to process analyzed image.")
            except Exception as e:
                st.error(f"Image Display Error: {e}")
        else:
            st.info("No annotated image returned.")

    # --- 4. WEATHER & AI ---
    st.markdown("---")
    st.subheader("📍 Weather-Based Advice")
    user_location = st.text_input("Enter location (e.g., Lucknow):")

    if user_location:
        with st.spinner("🌦️ Fetching weather..."):
            weather_response = api_client.get_weather(user_location)

        if weather_response:
            loc = weather_response.get("location", {})
            st.session_state["lat"] = loc.get("lat")
            st.session_state["lon"] = loc.get("lon")
            
            st.json(weather_response.get("current_weather", {}))
            generate_ai_summary()
            
            if "agentic_summary" in st.session_state:
                st.markdown("---")
                st.info(st.session_state["agentic_summary"])
                st.write(st.session_state["agentic_full"])

def generate_ai_summary():
    if st.session_state.get("lat"):
        with st.spinner("🤖 Generating AI recommendation..."):
            ai_response = api_client.get_agentic_summary(
                lat=st.session_state["lat"],
                lon=st.session_state["lon"],
                disease=st.session_state["disease"],
                confidence=st.session_state["confidence"]
            )
        if ai_response:
            st.session_state["agentic_summary"] = ai_response.get("summary")
            st.session_state["agentic_full"] = ai_response.get("recommendation")