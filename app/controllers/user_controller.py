from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from dotenv import load_dotenv
import os

user_bp = Blueprint("user", __name__)
load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def verify_token():
    # Allow OPTIONS requests to pass through
    if request.method == "OPTIONS":
        return None
    token = request.headers.get("X-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

@user_bp.route("/users", methods=["GET"])
def get_users():
    auth = verify_token()
    if auth:
        return auth
    users = UserService.get_all_users()
    return jsonify(users), 200

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = UserService.create_user(data)
    
    if isinstance(new_user, tuple):
        return jsonify(new_user[0]), new_user[1]

    return jsonify(new_user), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    response = UserService.get_user_by_id(user_id)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    return jsonify(response), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    response = UserService.update_user(user_id, data)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    return jsonify(response), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = UserService.delete_user(user_id)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    return jsonify(response), 200