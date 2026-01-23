"""
plant_yolo_model.py

Objective:
    Load the trained YOLOv8 model and perform plant disease detection.

Input:
    image_path (str): Path to uploaded image file.

Output:
    dict: Detection results (disease, confidence) and annotated image path.
"""

import os
from ultralytics import YOLO

# ✅ Base directory of this file (ml_model/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Point to the model inside ml_model/model/
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")

# ✅ Verify model path
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file not found at {MODEL_PATH}")

# ✅ Load YOLO model
model = YOLO(MODEL_PATH)

# ✅ Create output folder inside ml_model/outputs
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def predict_disease_yolo(image_path):
    """
    Run YOLO detection on plant leaf image and return results.
    """
    results = model.predict(
        source=image_path,
        save=True,
        project=OUTPUT_FOLDER,
        name="detections",
        exist_ok=True
    )

    detections = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls]
        detections.append({
            "disease": label,
            "confidence": round(conf * 100, 2)
        })

    # ✅ FIXED LINE — using os.path.join instead of /
    annotated_image_path = os.path.join(results[0].save_dir, os.path.basename(image_path))
    
    #NEW
    #annotated_image_url = f"http://localhost:5000/outputs/detections/{os.path.basename(annotated_image_path)}"

    return {
        "detections": detections,
        "annotated_image": annotated_image_path #from _path to _url
    }
