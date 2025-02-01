import re
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def create_user(data):
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, data.get("email", "")):
            return {"error": "Invalid email format"}, 400

        return UserRepository.create_user(data)

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user

    @staticmethod
    def update_user(user_id, data):
        name, email = data.get("name"), data.get("email")
        if not name or not email:
            return {"error": "Name and email are required"}, 400

        updated = UserRepository.update_user(user_id, data)
        if not updated:
            return {"error": "User not found"}, 404
        return {"message": "User updated successfully"}

    @staticmethod
    def delete_user(user_id):
        deleted = UserRepository.delete_user(user_id)
        if not deleted:
            return {"error": "User not found"}, 404
        return {"message": "User deleted successfully"}
