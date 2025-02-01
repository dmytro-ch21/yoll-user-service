from app.db import get_db

class MovieRepository:
    @staticmethod
    def add_movie(data):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO movies (title, genre, release_year, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
                (data["title"], data.get("genre"), data.get("release_year"), data["user_id"]),
            )
            movie_id = cursor.fetchone()[0]
            db.commit()
            return {
                "id": movie_id,
                "title": data["title"],
                "genre": data.get("genre"),
                "release_year": data.get("release_year"),
                "user_id": data["user_id"],
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
    
    @staticmethod
    def get_movies_by_user(user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT id, title, genre, release_year FROM movies WHERE user_id = %s",
                (user_id,),
            )
            movies = cursor.fetchall()
            return [
                {"id": m[0], "title": m[1], "genre": m[2], "release_year": m[3]}
                for m in movies
            ]
        finally:
            cursor.close()

    @staticmethod
    def delete_movie(movie_id, user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            # First, verify the movie exists for the given user
            cursor.execute(
                "SELECT id FROM movies WHERE id = %s AND user_id = %s", (movie_id, user_id)
            )
            movie = cursor.fetchone()
            if not movie:
                return None
            # Delete the movie
            cursor.execute(
                "DELETE FROM movies WHERE id = %s AND user_id = %s RETURNING id",
                (movie_id, user_id),
            )
            deleted = cursor.fetchone()
            db.commit()
            return deleted[0] if deleted else None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()        