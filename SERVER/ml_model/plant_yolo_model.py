"""
plant_yolo_model.py

Objective:
    Call the Hugging Face Gradio app to perform plant disease detection
    instead of running YOLO locally.

Input:
    image_path (str): Path to uploaded image file.

Output:
    dict:
        - detections: list of detected diseases with confidence
        - annotated_image: local path to annotated image
        - error (optional): if something goes wrong
"""

import os
import shutil
from gradio_client import Client, handle_file
from typing import Dict, Any

# ==========================================================
# CONFIG
# ==========================================================

HF_SPACE_ID = "Ayushi-begin/plant-scanner-model"   # Your Hugging Face Space ID
client = Client(HF_SPACE_ID)

# Local folder to store returned annotated images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================================
# FUNCTION
# ==========================================================

def predict_disease_yolo(image_path: str) -> Dict[str, Any]:
    """
    Send an image to the Hugging Face YOLO model and return results.

    Args:
        image_path (str): Path to the input image.

    Returns:
        dict: {
            "detections": list of dicts containing detected diseases and confidence,
            "annotated_image": str, local path to the annotated image,
            "error": optional str if an error occurs
        }
    """

    if not os.path.isfile(image_path):
        return {"error": f"Input image not found: {image_path}"}

    try:
        # Send image to Hugging Face Gradio API
        result = client.predict(
            handle_file(image_path),
            api_name="/predict"
        )

        # HF returns:
        # result[0] -> annotated image (temporary path)
        # result[1] -> detections (list of dicts)
        annotated_temp_path = result[0]
        detections = result[1]

        # Save annotated image locally
        local_image_name = f"annotated_{os.path.basename(image_path)}"
        local_image_path = os.path.join(OUTPUT_FOLDER, local_image_name)
        shutil.copy(annotated_temp_path, local_image_path)

        return {
            "detections": detections,
            "annotated_image": local_image_path
        }

    except Exception as e:
        # Friendly message if HF model is loading/waking up
        return {
            "error": "Model is waking up. Please try again in 30–60 seconds.",
            "details": str(e)
        }
