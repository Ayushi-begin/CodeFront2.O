"""
plant_yolo_model.py
"""

import os
import shutil
from gradio_client import Client

# ✅ Base directory (ml_model/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Output folder: ml_model/outputs/detections
# We match the folder structure your original code created
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "detections")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def predict_disease_yolo(image_path):
    """
    Sends image to Hugging Face, downloads the annotated result, 
    and saves it locally to match the professor's demo requirements.
    """
    
    # ---------------------------------------------------------
    # 1. Connect to Hugging Face (The Remote GPU)
    # ---------------------------------------------------------
    # 👇 CHANGE THIS to your specific Space name (e.g. "ayushi/plant-health")
    client = Client("Ayushi-begin/plant-scanner-model") 
    
    try:
        # ---------------------------------------------------------
        # 2. Get Prediction (Image + JSON)
        # ---------------------------------------------------------
        # The API returns a list: [path_to_downloaded_image, json_data]
        result = client.predict(
            image_path, 
            api_name="/predict"
        )
        
        temp_annotated_img_path = result[0] # The image file downloaded from HF
        detections_data = result[1]         # The list of diseases
        
        # ---------------------------------------------------------
        # 3. Save Image to Local Folder (Mimic YOLO logic)
        # ---------------------------------------------------------
        # Create a unique filename based on the input
        filename = os.path.basename(image_path)
        final_image_path = os.path.join(OUTPUT_DIR, filename)
        
        # Move the downloaded file to your project folder
        shutil.move(temp_annotated_img_path, final_image_path)
        
        # ---------------------------------------------------------
        # 4. Return EXACT Format expected by Frontend
        # ---------------------------------------------------------
        return {
            "detections": detections_data,
            "annotated_image": final_image_path
        }

    except Exception as e:
        print(f"❌ Error in Remote Prediction: {e}")
        # Fallback to prevent crash
        return {
            "detections": [{"disease": "Error", "confidence": 0}],
            "annotated_image": image_path 
        }