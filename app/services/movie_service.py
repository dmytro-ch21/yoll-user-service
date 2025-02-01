from app.repositories.movie_repository import MovieRepository

class MovieService:
    @staticmethod
    def add_movie(data):
        # Validate required fields
        if not data.get("title") or not data.get("user_id"):
            return {"error": "Title and user_id are required"}, 400
        try:
            movie = MovieRepository.add_movie(data)
            return movie
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_movies(user_id):
        if not user_id:
            return {"error": "User ID is required as a query parameter"}, 400
        movies = MovieRepository.get_movies_by_user(user_id)
        if not movies:
            return {"error": "No movies found for this user"}, 404
        return movies

    @staticmethod
    def delete_movie(movie_id, user_id):
        if not user_id:
            return {"error": "User ID is required to delete a movie"}, 400
        deleted = MovieRepository.delete_movie(movie_id, user_id)
        if not deleted:
            return {"error": "Movie not found or does not belong to this user"}, 404
        return {"message": "Movie deleted successfully"}