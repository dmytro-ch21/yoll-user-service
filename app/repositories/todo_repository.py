from app.db import get_db


class TodoRepository:
    @staticmethod
    def create_todo(data):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO todos (title, completed, user_id) VALUES (%s, %s, %s) RETURNING id, created_at",
                (data["title"], data.get("completed", False), data["user_id"]),
            )
            todo = cursor.fetchone()
            todo_id = todo[0]
            created_at = todo[1]
            db.commit()
            return {
                "id": todo_id,
                "title": data["title"],
                "completed": data.get("completed", False),
                "user_id": data["user_id"],
                "created_at": created_at,
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_all_todos(user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT id, title, completed, created_at FROM todos WHERE user_id = %s",
                (user_id,),
            )
            todos = cursor.fetchall()
            return [
                {"id": t[0], "title": t[1], "completed": t[2], "created_at": t[3]}
                for t in todos
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_todo_by_id(todo_id, user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT id, title, completed, created_at FROM todos WHERE id = %s AND user_id = %s",
                (todo_id, user_id),
            )
            todo = cursor.fetchone()
            if todo:
                return {
                    "id": todo[0],
                    "title": todo[1],
                    "completed": todo[2],
                    "created_at": todo[3],
                }
            else:
                return None
        finally:
            cursor.close()

    @staticmethod
    def update_todo(todo_id, user_id, data):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                UPDATE todos 
                SET title = %s, completed = %s 
                WHERE id = %s AND user_id = %s 
                RETURNING id, title, completed, created_at
                """,
                (data["title"], data.get("completed", False), todo_id, user_id),
            )
            updated = cursor.fetchone()
            db.commit()
            if updated:
                return {
                    "id": updated[0],
                    "title": updated[1],
                    "completed": updated[2],
                    "created_at": updated[3],
                }
            return None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete_todo(todo_id, user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "DELETE FROM todos WHERE id = %s AND user_id = %s RETURNING id",
                (todo_id, user_id),
            )
            deleted = cursor.fetchone()
            db.commit()
            return deleted[0] if deleted else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
