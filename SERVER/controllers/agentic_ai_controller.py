# ==================================================
# FILE: controllers/agentic_ai_controller.py
# ==================================================
from flask import request, jsonify
from services.agentic_ai_service import run_agentic_analysis

def process_agentic_ai():
    """
    Handles Agentic AI requests combining:
    - YOLO results
    - Weather info
    - MongoDB history
    """
    data = request.get_json()

    lat = data.get("lat")
    lon = data.get("lon")
    disease = data.get("disease")
    confidence = data.get("confidence")

    if lat is None or lon is None or not disease or confidence is None:
        return jsonify({"error": "Missing parameters"}), 400
    
    
    #*100 because the value of the confidence is passed as percentage in the parameter of agentic_ai.
    result = run_agentic_analysis(lat, lon, disease, confidence)
    #return jsonify(result), 200


    # ✅ --- MODIFICATION STARTS HERE ---
    # Create a short summary for frontend (first 2 lines or 250 chars)
    full_recommendation = result.get("recommendation", "")
    summary = full_recommendation.split("\n\n")[0][:250] + "..." if full_recommendation else ""

    # Return both summary (for frontend) and full recommendation
    return jsonify({
        "summary": summary,
        "recommendation": full_recommendation
    }), 200
    # ✅ --- MODIFICATION ENDS HERE ---