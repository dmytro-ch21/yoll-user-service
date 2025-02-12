from app.db import get_db

class ContactsFavoritesRepository:
    @staticmethod
    def add_favorite(user_id, contact_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO contacts_favorites (user_id, contact_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING contact_id;
                """,
                (user_id, contact_id)
            )
            result = cursor.fetchone()
            db.commit()
            return result[0] if result else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete_favorite(user_id, contact_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM contacts_favorites
                WHERE user_id = %s AND contact_id = %s
                RETURNING contact_id;
                """,
                (user_id, contact_id)
            )
            result = cursor.fetchone()
            db.commit()
            return result[0] if result else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_favorites_by_user(user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                SELECT c.id, c.full_name, c.email, c.phone_number, c.created_at, c.is_favorite
                FROM contacts c
                INNER JOIN contacts_favorites cf ON c.id = cf.contact_id
                WHERE cf.user_id = %s;
                """,
                (user_id,)
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "full_name": row[1],
                    "email": row[2],
                    "phone_number": row[3],
                    "created_at": row[4],
                    "is_favorite": row[5],
                }
                for row in rows
            ]
        finally:
            cursor.close()
