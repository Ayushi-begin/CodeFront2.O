import os
import shutil
import base64
from gradio_client import Client

# ✅ Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "detections")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def predict_disease_yolo(image_path):
    # 1. Connect to Hugging Face
    client = Client("Ayushi-begin/plant-scanner-model") 
    
    try:
        # 2. Get Prediction
        result = client.predict(image_path, api_name="/predict")
        
        temp_annotated_img_path = result[0]
        detections_data = result[1]
        
        # 3. Save locally (optional, but good for debug)
        filename = os.path.basename(image_path)
        final_image_path = os.path.join(OUTPUT_DIR, filename)
        shutil.move(temp_annotated_img_path, final_image_path)
        
        # 4. CONVERT TO BASE64 (The Fix 🛠️)
        with open(final_image_path, "rb") as img_file:
            # Convert the actual image file to a text string
            b64_string = base64.b64encode(img_file.read()).decode('utf-8')
        
        return {
            "detections": detections_data,
            "annotated_image": b64_string  # ✅ Sending DATA, not a path
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "detections": [{"disease": "Error", "confidence": 0}],
            "annotated_image": None 
        }