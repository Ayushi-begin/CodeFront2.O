#history_routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config.db import history_db

history_bp = Blueprint("history", __name__)

# -----------------------------------------
# Save history entry
# -----------------------------------------
@history_bp.route("/save-history", methods=["POST"])
def save_history():
    data = request.json

    data["timestamp"] = datetime.utcnow()
    result = history_db["history"].insert_one(data)

    return jsonify({"message": "saved", "id": str(result.inserted_id)}), 200


# -----------------------------------------
# Get full history
# -----------------------------------------
@history_bp.route("/get-history", methods=["GET"])
def get_history():
    records = list(history_db["history"].find().sort("timestamp", -1))

    # Convert ObjectId → string
    for r in records:
        r["_id"] = str(r["_id"])

    return jsonify(records), 200


# -----------------------------------------
# Delete one history item
# -----------------------------------------
@history_bp.route("/delete-history", methods=["DELETE"])
def delete_history():
    record_id = request.args.get("id")

    history_db["history"].delete_one({"_id": ObjectId(record_id)})

    return jsonify({"message": "deleted"}), 200


# -----------------------------------------
# Delete ALL history
# -----------------------------------------
@history_bp.route("/delete-all-history", methods=["DELETE"])
def delete_all_history():
    history_db["history"].delete_many({})

    return jsonify({"message": "all deleted"}), 200
