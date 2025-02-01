from app.db import get_db

class UserRepository:
    @staticmethod
    def get_all_users():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email FROM users;")
        users = cursor.fetchall()
        cursor.close()
        return [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
    
    @staticmethod
    def create_user(data):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;", (data["name"], data["email"]))
        user_id = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        return {"id": user_id, "name": data["name"], "email": data["email"]}
        