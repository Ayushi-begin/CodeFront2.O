import streamlit as st
import base64 # ✅ Import this
from utils.api_client import get_history, delete_history, delete_all_history

def render():
    st.title("📜 Your History")

    # DELETE ALL BUTTON
    if st.button("🗑️ Delete Entire History"):
        if delete_all_history():
            st.success("All records deleted!")
            st.rerun() # updated from experimental_rerun
        else:
            st.error("Failed to delete history.")

    st.markdown("---")

    records = get_history()

    if not records:
        st.info("No history available.")
        return

    for entry in records:
        # ✅ HANDLE IMAGE DISPLAY (Base64)
        if "annotated_image" in entry and entry["annotated_image"]:
            try:
                # If it's a long base64 string
                img_bytes = base64.b64decode(entry["annotated_image"])
                st.image(img_bytes, caption="Historical Analysis")
            except:
                st.error("Error loading image data.")
        else:
            st.warning("Image not available for this record.")

        st.subheader("🩺 Detected Diseases")
        if "detections" in entry:
            for det in entry["detections"]:
                st.write(f"- {det.get('disease', 'Unknown')} ({det.get('confidence', 0)}%)")

        st.subheader("🌱 Summary")
        st.write(entry.get("summary", "No summary available."))

        with st.expander("📄 Full Recommendation"):
            st.write(entry.get("full_recommendation", "No recommendation available."))

        # DELETE SINGLE BUTTON
        if st.button("🗑️ Delete This Record", key=str(entry.get("_id"))):
            if delete_history(entry.get("_id")):
                st.success("Record deleted!")
                st.rerun()
            else:
                st.error("Failed to delete this record.")

        st.markdown("---")