from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")
DELETE_SECRET_TOKEN = os.getenv("DELETE_SECRET_TOKEN")

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Allow OPTIONS requests to pass through
        if request.method == "OPTIONS":
            return func(*args, **kwargs)
        token = request.headers.get("X-Secret-Token")
        if token != SECRET_TOKEN:
            return jsonify({"error": "Unauthorized"}), 403
        return func(*args, **kwargs)
    return wrapper

def require_delete_privileges(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delete_token = request.headers.get("X-Delete-Token")
        print(f"Received delete_token: {delete_token} | Expected: {DELETE_SECRET_TOKEN}")
        if delete_token != DELETE_SECRET_TOKEN:
            return jsonify({"error": "Insufficient privileges for delete operation"}), 403
        return func(*args, **kwargs)
    return wrapper
