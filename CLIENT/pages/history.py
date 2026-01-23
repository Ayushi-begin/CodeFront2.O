import streamlit as st
from utils.api_client import get_history, delete_history, delete_all_history

def render():
    st.title("📜 Your History")

    # DELETE ALL BUTTON
    if st.button("🗑️ Delete Entire History"):
        if delete_all_history():
            st.success("All records deleted!")
            st.experimental_rerun()
        else:
            st.error("Failed to delete history.")

    st.markdown("---")

    records = get_history()

    if not records:
        st.info("No history available.")
        return

    for entry in records:
        st.image(entry["annotated_image"])

        st.subheader("🩺 Detected Diseases")
        for det in entry["detections"]:
            st.write(f"- {det['disease']} ({det['confidence']}%)")

        

        st.subheader("🌱 Summary")
        st.write(entry["summary"])

        with st.expander("📄 Full Recommendation"):
            st.write(entry["full_recommendation"])

        # DELETE SINGLE BUTTON
        if st.button("🗑️ Delete This Record", key=entry["_id"]):
            if delete_history(entry["_id"]):
                st.success("Record deleted!")
                st.experimental_rerun()
            else:
                st.error("Failed to delete this record.")

        st.markdown("---")
