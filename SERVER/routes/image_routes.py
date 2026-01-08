from flask import Blueprint
from controllers.image_controller import process_image

image_bp = Blueprint("image_bp", __name__)

@image_bp.route("/upload", methods=["POST"])
def upload_image():
    """Handles plant image uploads and triggers YOLO prediction"""
    return process_image()
