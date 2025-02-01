import re
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()
    
    @staticmethod
    def create_user(data):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, data.get("email", "")):
            return {"error": "Invalid email format"}, 400

        return UserRepository.create_user(data)