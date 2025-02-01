# app/services/todo_service.py
from app.repositories.todo_repository import TodoRepository

class TodoService:
    @staticmethod
    def create_todo(data):
        if not data.get("task") or not data.get("user_id"):
            return {"error": "Task and user_id are required"}, 400
        try:
            todo = TodoRepository.create_todo(data)
            return todo
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_all_todos(user_id):
        if not user_id:
            return {"error": "User ID is required as a query parameter"}, 400
        todos = TodoRepository.get_all_todos(user_id)
        if not todos:
            return {"error": "No todos found for this user"}, 404
        return todos

    @staticmethod
    def get_todo_by_id(todo_id, user_id):
        if not user_id:
            return {"error": "User ID is required"}, 400
        todo = TodoRepository.get_todo_by_id(todo_id, user_id)
        if not todo:
            return {"error": "Todo not found"}, 404
        return todo

    @staticmethod
    def update_todo(todo_id, user_id, data):
        if not data.get("task"):
            return {"error": "Task is required"}, 400
        updated = TodoRepository.update_todo(todo_id, user_id, data)
        if not updated:
            return {"error": "Todo not found or update failed"}, 404
        return {"message": "Todo updated successfully"}

    @staticmethod
    def delete_todo(todo_id, user_id):
        deleted = TodoRepository.delete_todo(todo_id, user_id)
        if not deleted:
            return {"error": "Todo not found or does not belong to this user"}, 404
        return {"message": "Todo deleted successfully"}