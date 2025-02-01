import os
from flask import Blueprint, request, jsonify, current_app
from app.db import get_db 
from dotenv import load_dotenv
from app.services.user_service import UserService


user_bp = Blueprint("user", __name__)
load_dotenv()

routes_bp = Blueprint('routes', __name__)
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def verify_token():
    """Check if the request contains a valid secret token."""
    token = request.headers.get("X-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

@routes_bp.route('/')
def home():
    return "Flask App is Running!"

### 🔹 USERS API ###
@routes_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    name, email = data.get('name'), data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
        user_id = cursor.fetchone()[0]
        db.commit()
        return jsonify({"id": user_id, "message": "User created successfully", "note": "Save the id, you will need it for further requests"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        
@user_bp.route('/users', methods=['GET'])
def get_all_users():
    """Retrieve all users"""
    auth = verify_token()
    if auth:
        return auth  # Return 403 if unauthorized
    
    users = UserService.get_all_users()
    return jsonify(users), 200

@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by ID"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user details"""
    data = request.json
    name, email = data.get('name'), data.get('email')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id", (name, email, user_id))
    updated = cursor.fetchone()
    db.commit()
    cursor.close()

    if updated:
        return jsonify({"message": "User updated successfully"})
    return jsonify({"error": "User not found"}), 404

@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    auth = verify_token()
    if auth:
        return auth  # Return 403 if unauthorized
    
    """Delete a user"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()

    if deleted:
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404


### 🔹 MOVIES API ###
@routes_bp.route('/movies', methods=['POST'])
def add_movie():
    """Add a new movie"""
    data = request.json
    title, genre, release_year, user_id = data.get('title'), data.get('genre'), data.get('release_year'), data.get('user_id')

    if not title or not user_id:
        return jsonify({"error": "Title and user_id are required"}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO movies (title, genre, release_year, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
                       (title, genre, release_year, user_id))
        movie_id = cursor.fetchone()[0]
        db.commit()
        return jsonify({"id": movie_id, "message": "Movie added successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

@routes_bp.route('/movies', methods=['GET'])
def get_movies():
    """Retrieve movies for a specific user (Requires `user_id` as a query parameter)"""
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required as a query parameter"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, title, genre, release_year FROM movies WHERE user_id = %s", (user_id,))
    movies = cursor.fetchall()
    cursor.close()

    if not movies:
        return jsonify({"error": "No movies found for this user"}), 404

    movie_list = [{"id": m[0], "title": m[1], "genre": m[2], "release_year": m[3]} for m in movies]
    return jsonify(movie_list), 200

@routes_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """Delete a movie (requires `user_id` as a query parameter)"""

    user_id = request.args.get('user_id')  # Retrieve user_id from query parameters

    if not user_id:
        return jsonify({"error": "User ID is required to delete a movie"}), 400

    db = get_db()
    cursor = db.cursor()

    # Ensure that the movie exists and belongs to the user
    cursor.execute("SELECT id FROM movies WHERE id = %s AND user_id = %s", (movie_id, user_id))
    movie = cursor.fetchone()

    if not movie:
        return jsonify({"error": "Movie not found or does not belong to this user"}), 404

    # Delete the movie
    cursor.execute("DELETE FROM movies WHERE id = %s AND user_id = %s RETURNING id", (movie_id, user_id))
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()

    if deleted:
        return jsonify({"message": "Movie deleted successfully"})
    return jsonify({"error": "Movie not found"}), 404