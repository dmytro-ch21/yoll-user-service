from flask import Blueprint, request, jsonify
from app.services.contact_favorites_service import ContactsFavoritesService

contacts_favorites_bp = Blueprint("contacts_favorites", __name__)

@contacts_favorites_bp.route("/contacts-favorites", methods=["POST"])
def add_favorite():
    data = request.json
    # JSON payload should include "user_id" and "contact_id"
    user_id = data.get("user_id")
    contact_id = data.get("contact_id")
    if not user_id or not contact_id:
        return jsonify({"error": "user_id and contact_id are required"}), 400
    result = ContactsFavoritesService.add_favorite(user_id, contact_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 201

@contacts_favorites_bp.route("/contacts-favorites/<int:contact_id>", methods=["DELETE"])
def delete_favorite(contact_id):
    # user_id is provided via a query parameter
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required as query parameter"}), 400
    result = ContactsFavoritesService.delete_favorite(int(user_id), contact_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@contacts_favorites_bp.route("/contacts-favorites", methods=["GET"])
def get_favorites():
    # Assume user_id is provided via query parameter
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    result = ContactsFavoritesService.get_favorites(int(user_id))
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
