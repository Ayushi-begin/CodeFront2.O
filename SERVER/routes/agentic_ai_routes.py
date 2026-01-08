# ==================================================
# FILE: routes/agentic_ai_routes.py
# ==================================================
from flask import Blueprint
from controllers.agentic_ai_controller import process_agentic_ai

agentic_ai_bp = Blueprint("agentic_ai_bp", __name__)

@agentic_ai_bp.route("/agentic-ai", methods=["POST"])
def agentic_ai_route():
    """API endpoint for agentic AI reasoning"""
    return process_agentic_ai()

