# app/controllers/todo_controller.py
from flask import Blueprint, request, jsonify
from app.services.todo_service import TodoService

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/todos", methods=["POST"])
def create_todo():
    data = request.json
    result = TodoService.create_todo(data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 201


@todo_bp.route("/todos", methods=["GET"])
def get_all_todos():
    user_id = request.args.get("user_id")
    result = TodoService.get_all_todos(user_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@todo_bp.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    user_id = request.args.get("user_id")
    result = TodoService.get_todo_by_id(todo_id, user_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@todo_bp.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    user_id = request.args.get("user_id")
    data = request.json
    result = TodoService.update_todo(todo_id, user_id, data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@todo_bp.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    user_id = request.args.get("user_id")
    result = TodoService.delete_todo(todo_id, user_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
