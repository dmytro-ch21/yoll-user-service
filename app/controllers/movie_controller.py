from flask import Blueprint, request, jsonify
from app.services.movie_service import MovieService

movie_bp = Blueprint("movie", __name__)


@movie_bp.route("/movies", methods=["POST"])
def add_movie():
    data = request.json
    result = MovieService.add_movie(data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 201


@movie_bp.route("/movies", methods=["GET"])
def get_movies():
    user_id = request.args.get("user_id")
    result = MovieService.get_movies(user_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


@movie_bp.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    user_id = request.args.get("user_id")
    result = MovieService.delete_movie(movie_id, user_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
