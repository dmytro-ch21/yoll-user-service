from app.db import get_db

class ContactRepository:
    @staticmethod
    def create_contact(data):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO contacts (user_id, full_name, phone_number, email, street, city, state, postal_code, country, additional_info, base64_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, user_id, full_name, created_at;
                """,
                (
                    data.get("user_id"),
                    data.get("full_name"),
                    data.get("phone_number"),
                    data.get("email"),
                    data.get("street"),
                    data.get("city"),
                    data.get("state"),
                    data.get("postal_code"),
                    data.get("country"),
                    data.get("additional_info"),
                    data.get("base64_image"),
                ),
            )
            created_contact = cursor.fetchone()
            db.commit()
            return {"id": created_contact[0], "user_id": created_contact[1], "full_name": created_contact[2], "created_at": created_contact[3]}
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_all_contacts():
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                SELECT id, user_id, full_name, phone_number, email, street, city, state, postal_code, country, additional_info, base64_image, created_at 
                FROM contacts;
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "full_name": row[2],
                    "phone_number": row[3],
                    "email": row[4],
                    "street": row[5],
                    "city": row[6],
                    "state": row[7],
                    "postal_code": row[8],
                    "country": row[9],
                    "additional_info": row[10],
                    "base64_image": row[11],
                    "created_at": row[12],
                }
                for row in rows
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_contact_by_id(contact_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                SELECT id, user_id, full_name, phone_number, email, street, city, state, postal_code, country, additional_info, base64_image, created_at 
                FROM contacts WHERE id = %s;
                """,
                (contact_id,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "full_name": row[2],
                    "phone_number": row[3],
                    "email": row[4],
                    "street": row[5],
                    "city": row[6],
                    "state": row[7],
                    "postal_code": row[8],
                    "country": row[9],
                    "additional_info": row[10],
                    "base64_image": row[11],
                    "created_at": row[12],
                }
            return None
        finally:
            cursor.close()

    @staticmethod
    def update_contact(contact_id, data):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                UPDATE contacts
                SET full_name = %s, phone_number = %s, email = %s, street = %s, city = %s, state = %s, postal_code = %s, country = %s, additional_info = %s, base64_image = %s
                WHERE id = %s RETURNING id;
                """,
                (
                    data.get("full_name"),
                    data.get("phone_number"),
                    data.get("email"),
                    data.get("street"),
                    data.get("city"),
                    data.get("state"),
                    data.get("postal_code"),
                    data.get("country"),
                    data.get("additional_info"),
                    data.get("base64_image"),
                    contact_id,
                ),
            )
            updated = cursor.fetchone()
            db.commit()
            return updated[0] if updated else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete_contact(contact_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "DELETE FROM contacts WHERE id = %s RETURNING id;", (contact_id,)
            )
            deleted = cursor.fetchone()
            db.commit()
            return deleted[0] if deleted else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def update_favorite_status(contact_id, is_favorite):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE contacts SET is_favorite = %s WHERE id = %s RETURNING id;",
                (is_favorite, contact_id),
            )
            updated = cursor.fetchone()
            db.commit()
            return updated[0] if updated else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_all_contacts_by_user(user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                SELECT id, user_id, full_name, phone_number, email, city, country, base64_image, is_favorite
                FROM contacts WHERE user_id = %s;
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "full_name": row[2],
                    "phone_number": row[3],
                    "email": row[4],
                    "city": row[5],
                    "country": row[6],
                    "base64_image": row[7],
                    "is_favorite": row[8],
                }
                for row in rows
            ]
        finally:
            cursor.close()

    @staticmethod
    def get_contact_by_id_and_user(contact_id, user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                SELECT id, user_id, full_name, phone_number, email, street, city, state, postal_code, country, additional_info, base64_image, created_at, is_favorite
                FROM contacts WHERE id = %s AND user_id = %s;
                """,
                (contact_id, user_id),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "full_name": row[2],
                    "phone_number": row[3],
                    "email": row[4],
                    "street": row[5],
                    "city": row[6],
                    "state": row[7],
                    "postal_code": row[8],
                    "country": row[9],
                    "additional_info": row[10],
                    "base64_image": row[11],
                    "created_at": row[12],
                    "is_favorite": row[13],
                }
            return None
        finally:
            cursor.close()
