from flask import Blueprint, jsonify
from controllers.auth_controller import google_login, google_callback

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/auth/login')
def login():
    return google_login()

@auth_bp.route('/auth/callback')
def callback():
    user_info = google_callback()
    return jsonify({
        "message": "Login successful",
        "user_info": user_info
    })
