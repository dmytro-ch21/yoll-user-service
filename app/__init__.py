import os
from flask import Flask
from flask_cors import CORS
from app.db import close_db
from dotenv import load_dotenv
from .logging_config import configure_logging
from flask_swagger_ui import get_swaggerui_blueprint
from app.controllers.todo_controller import todo_bp
from app.controllers.user_controller import user_bp
from app.controllers.movie_controller import movie_bp
from app.controllers.default_controller import default_bp

load_dotenv()

def create_app():
    """Initialize Flask app"""
    app = Flask(__name__)

    CORS(app)

    configure_logging(app)

    app.config["DATABASE"] = {
        "dbname": os.getenv("DATABASE_NAME"),
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "host": os.getenv("DATABASE_HOST"),
        "port": os.getenv("DATABASE_PORT"),
    }

    app.register_blueprint(default_bp)
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(movie_bp, url_prefix="/api")
    app.register_blueprint(todo_bp, url_prefix="/api")

    SWAGGER_URL = "/api/docs"  
    API_URL = (
        "/static/openapi.json"  
    )
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Yoll User Service API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    app.teardown_appcontext(close_db)

    return app
