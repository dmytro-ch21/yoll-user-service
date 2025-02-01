from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = UserService.get_all_users()
    return jsonify(users), 200

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = UserService.create_user(data)
    
    if isinstance(new_user, tuple):
        return jsonify(new_user[0]), new_user[1]

    return jsonify(new_user), 201