"""
Objective:
    Displays past analysis records.
    FIX: Handles Base64 images safely and prevents crashes on missing files.
"""

import streamlit as st
import base64
import io
import numpy as np
from PIL import Image
from utils.api_client import get_history, delete_history, delete_all_history

# ==========================================================
# 🛡️ HELPER: FORCE TO NUMPY ARRAY (BULLETPROOF)
# ==========================================================
def load_safe_image(image_data):
    """
    Converts ANY input (Bytes, Base64) into a Numpy Array.
    Prevents Streamlit crashes by stripping file metadata.
    """
    try:
        image_obj = None

        # Case 1: Raw Bytes
        if isinstance(image_data, bytes):
            image_obj = Image.open(io.BytesIO(image_data))
        
        # Case 2: Already a PIL Image
        elif isinstance(image_data, Image.Image):
            image_obj = image_data

        # Convert to Numpy Array (Streamlit loves this)
        if image_obj:
            return np.array(image_obj.convert("RGB"))
            
        return None

    except Exception as e:
        return None

# ==========================================================
# 📜 RENDER HISTORY PAGE
# ==========================================================
def render():
    st.title("📜 Your History")

    # --- DELETE ALL BUTTON ---
    if st.button("🗑️ Delete Entire History", type="secondary"):
        if delete_all_history():
            st.success("All records deleted!")
            st.rerun()
        else:
            st.error("Failed to delete history.")

    st.markdown("---")

    # --- FETCH RECORDS ---
    records = get_history()

    if not records:
        st.info("No history available yet.")
        return

    # --- DISPLAY RECORDS ---
    for entry in reversed(records):  # Show newest first
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])

            # --- IMAGE COLUMN ---
            with col1:
                # 1. Try to get the Base64 image data
                b64_data = entry.get("annotated_image")
                
                # 2. Check if it's a valid string (not a file path!)
                # If it's short (< 200 chars), it's likely a file path (BROKEN on cloud)
                # If it's long (> 200 chars), it's likely Base64 data (GOOD)
                if b64_data and isinstance(b64_data, str) and len(b64_data) > 200:
                    try:
                        # Clean header if present
                        if "," in b64_data:
                            b64_data = b64_data.split(",")[1]
                        
                        # Decode and Safe Load
                        img_bytes = base64.b64decode(b64_data)
                        numpy_img = load_safe_image(img_bytes)
                        
                        if numpy_img is not None:
                            st.image(numpy_img, caption="Analysis Result", use_container_width=True)
                        else:
                            st.warning("⚠️ Image corrupted")
                    except Exception:
                        st.warning("⚠️ Image error")
                else:
                    # Fallback for old records or missing data
                    st.info("🖼️ Image not available (Old Record)")

            # --- DATA COLUMN ---
            with col2:
                # Date (if available)
                timestamp = entry.get("timestamp", "")
                if timestamp:
                    st.caption(f"📅 ID: {timestamp}")

                # Detections
                st.subheader("🩺 Detected Diseases")
                detections = entry.get("detections", [])
                if detections:
                    for det in detections:
                        d_name = det.get('disease', 'Unknown')
                        d_conf = det.get('confidence', 0)
                        st.write(f"• **{d_name}** ({d_conf}%)")
                else:
                    st.write("No diseases detected.")

                # Summary
                st.subheader("🌱 Summary")
                st.write(entry.get("recommendation", "No summary available."))

                # Delete Button
                if st.button("🗑️ Delete", key=f"del_{entry.get('_id')}"):
                    if delete_history(entry.get("_id")):
                        st.rerun()