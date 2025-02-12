from flask import Blueprint, request, jsonify
from app.services.contact_favorites_service import ContactsFavoritesService

user_contacts_favorites_bp = Blueprint("user_contacts_favorites", __name__)

@user_contacts_favorites_bp.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.json
    if not data.get("user_id") or not data.get("contact_id"):
        return jsonify({"error": "user_id and contact_id are required"}), 400
    result = ContactsFavoritesService.add_favorite(data["user_id"], data["contact_id"])
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 201

@user_contacts_favorites_bp.route("/favorites", methods=["GET"])
def get_favorites():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required as a query parameter"}), 400
    result = ContactsFavoritesService.get_favorites(user_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_contacts_favorites_bp.route("/favorites/<int:contact_id>", methods=["DELETE"])
def delete_favorite(contact_id):
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required as a query parameter"}), 400
    result = ContactsFavoritesService.delete_favorite(int(user_id), contact_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
