from flask import Blueprint, request, jsonify
from app.services.contact_service import ContactService

user_contact_bp = Blueprint("contact", __name__)


@user_contact_bp.route("/secret/contacts", methods=["GET"])
def get_all_contacts_secret():
    result = ContactService.get_all_contacts()
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@user_contact_bp.route("/contacts", methods=["POST"])
def create_contact():
    data = request.json
    if not data or not data.get("user_id") or not data.get("full_name"):
        return (
            jsonify({"error": "user_id and full_name are required in the payload"}),
            400,
        )
    result = ContactService.create_contact(data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 201


@user_contact_bp.route("/contacts", methods=["GET"])
def get_all_contacts():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required as a query parameter"}), 400
    result = ContactService.get_all_contacts_by_user(int(user_id))
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@user_contact_bp.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required as a query parameter"}), 400
    result = ContactService.get_contact_by_id_and_user(contact_id, int(user_id))
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@user_contact_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.json or {}
    if not data.get("user_id"):
        return jsonify({"error": "user_id is required in the payload"}), 400
    result = ContactService.update_contact(contact_id, data, int(data["user_id"]))
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@user_contact_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required as a query parameter"}), 400
    result = ContactService.delete_contact(contact_id, int(user_id))
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
