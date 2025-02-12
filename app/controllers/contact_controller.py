from flask import Blueprint, request, jsonify
from app.services.contact_service import ContactService

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contacts", methods=["POST"])
def create_contact():
    data = request.json
    result = ContactService.create_contact(data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 201

@contact_bp.route("/contacts", methods=["GET"])
def get_all_contacts():
    result = ContactService.get_all_contacts()
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@contact_bp.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    result = ContactService.get_contact_by_id(contact_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@contact_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.json
    result = ContactService.update_contact(contact_id, data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@contact_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    result = ContactService.delete_contact(contact_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
