# ==========================================================
# FILE: frontend/pages/results.py
# ==========================================================
"""
Objective:
    Display YOLO detection results, weather details, and AI-generated advice.
    Includes Frontend-only TTS with Stop button and fixed history saving logic.
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.api_client import save_history_to_backend
import json  # For safely escaping TTS text

def render():
    """Render the Results Page to show YOLO results and AI analysis."""

    # ----------------------------------------------------------
    # 1️⃣ Ensure YOLO Results Exist
    # ----------------------------------------------------------
    if not st.session_state.get("yolo_result"):
        st.warning("⚠️ No detection results found. Please scan an image first.")
        return

    yolo_data = st.session_state["yolo_result"]
    detections = yolo_data.get("detections", [])
    annotated_image = yolo_data.get("annotated_image")
    message = yolo_data.get("message", "")

    st.title("🌿 AI Analysis Results")
    st.info(message or "Image processed successfully!")

    # ----------------------------------------------------------
    # 2️⃣ Display Annotated Image
    # ----------------------------------------------------------
    if annotated_image:
        st.image(annotated_image, caption="Detected Image", width="stretch")

    # ----------------------------------------------------------
    # 3️⃣ Display Detected Diseases
    # ----------------------------------------------------------
    if detections:
        st.subheader("🩺 Detected Diseases:")
        for det in detections:
            disease = det.get("disease", "Unknown")
            confidence = det.get("confidence", 0)
            st.markdown(f"- **{disease}** ({confidence:.2f}%)")
    else:
        st.warning("No diseases detected in the image.")

    st.markdown("---")

    # ----------------------------------------------------------
    # 4️⃣ AI Summary Recommendation
    # ----------------------------------------------------------
    summary_text = st.session_state.get("agentic_full", "")  # FULL recommendation

    if summary_text:
        st.markdown(
            f"""
            <div style='padding:18px; border-radius:12px;
                        background-color:#E8F5E9; color:#1B5E20;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);'>
                <h4>🌱 <b>AI Recommendation:</b></h4>
                <p>{summary_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------------------------------
    # 5️⃣ Full Recommendation (Expandable)
    # ----------------------------------------------------------
    with st.expander("🧾 View Full Recommendation"):
        full_text = st.session_state.get("agentic_full", "No full recommendation available.")
        st.write(full_text)

    # ----------------------------------------------------------
    # 🔊 Frontend-Only Text-to-Speech (Speak + Stop)
    # ----------------------------------------------------------
    if summary_text:
        clean_text_js = json.dumps(summary_text)  # Safely escape long text

        tts_html = f"""
        <div style="background-color: #f1f8e9; padding: 12px; border-radius: 10px; border: 1px solid #c8e6c9; margin: 15px 0;">
            <span style="font-family: sans-serif; font-weight: bold; color: #2e7d32;">🔊 Voice Guidance:</span>
            <select id="voiceSelect" style="margin-left: 8px; padding: 4px; border-radius: 4px; border: 1px solid #ddd;">
                <option value="en-US">English (US)</option>
                <option value="hi-IN">Hindi (भारत)</option>
            </select>
            <button id="speakBtn" style="
                margin-left: 8px; padding: 6px 14px; background-color: #43a047; 
                color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                Listen to Advice
            </button>
            <button id="stopBtn" style="
                margin-left: 8px; padding: 6px 14px; background-color: #e53935; 
                color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                Stop Reading
            </button>
        </div>

        <script>
            const btnSpeak = document.getElementById('speakBtn');
            const btnStop = document.getElementById('stopBtn');
            const voiceSelect = document.getElementById('voiceSelect');
            const synth = window.speechSynthesis;

            btnSpeak.onclick = () => {{
                synth.cancel();
                const text = {clean_text_js};
                const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
                sentences.forEach(sentence => {{
                    const utterance = new SpeechSynthesisUtterance(sentence.trim());
                    utterance.lang = voiceSelect.value;
                    utterance.rate = 0.95;
                    utterance.pitch = 1.0;
                    synth.speak(utterance);
                }});
            }};

            btnStop.onclick = () => {{
                synth.cancel();
            }};
        </script>
        """

        components.html(tts_html, height=160)

    # ----------------------------------------------------------
    # 6️⃣ Save to History Button
    # ----------------------------------------------------------
    if st.button("💾 Save This Result to History"):
        history_entry = {
            "filename": yolo_data.get("filename"),
            "annotated_image": annotated_image, 
            "detections": detections,
            "weather": st.session_state.get("weather"),
            "summary": summary_text,
            "full_recommendation": st.session_state.get("agentic_full")
        }

        success = save_history_to_backend(history_entry)

        if success:
            st.success("✅ Saved to history")
