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
        
    @staticmethod
    def get_user_by_id(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s;", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return {"id": user[0], "name": user[1], "email": user[2]} if user else None

    @staticmethod
    def update_user(user_id, data):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id;",
            (data["name"], data["email"], user_id),
        )
        updated = cursor.fetchone()
        db.commit()
        cursor.close()
        return updated

    @staticmethod
    def delete_user(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
        deleted = cursor.fetchone()
        db.commit()
        cursor.close()
        return deleted
    
    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
        "SELECT id, name, email FROM users WHERE LOWER(email) = LOWER(%s);",(email,),)
        user = cursor.fetchone()
        cursor.close()
        return {"id": user[0], "name": user[1], "email": user[2]} if user else None