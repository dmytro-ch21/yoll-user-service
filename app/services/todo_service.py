from app.repositories.todo_repository import TodoRepository

class TodoService:
    @staticmethod
    def create_todo(data):
        if not data.get("title") or not data.get("user_id"):
            return {"error": "Fields title and user_id are required"}, 400
        try:
            todo = TodoRepository.create_todo(data)
            return todo
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_all_todos(user_id):
        if not user_id:
            return {"error": "user_id is required as a query parameter: /todos?user_id=<user_id>"}, 400
        todos = TodoRepository.get_all_todos(user_id)
        if not todos:
            return {"error": f"No todos found for this user_id={user_id}"}, 404
        return todos

    @staticmethod
    def get_todo_by_id(todo_id, user_id):
        if not user_id or not todo_id:
            return {"error": "user_id and todo_id are required"}, 400
        todo = TodoRepository.get_todo_by_id(todo_id, user_id)
        if not todo:
            return {"error": f"Todo with id={todo_id} not found"}, 404
        return todo

    @staticmethod
    def update_todo(todo_id, user_id, data):
        if not data.get("title"):
            return {"error": "Field title is required"}, 400
        updated = TodoRepository.update_todo(todo_id, user_id, data)
        if not updated:
            return {"error": f"Todo with id={todo_id} not found or update failed"}, 404
        return {"message": "Todo updated successfully", "task": updated}

    @staticmethod
    def delete_todo(todo_id, user_id):
        deleted = TodoRepository.delete_todo(todo_id, user_id)
        if not deleted:
            return {"error": f"Todo with id={todo_id} not found or does not belong to this user"}, 404
        return {"message": f"Todo with id={todo_id} deleted successfully"}
