import os
from flask import Flask
from app.controllers.user_controller import user_bp
from app.controllers.movie_controller import movie_bp
from app.controllers.todo_controller import todo_bp
from app.db import close_db 
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from .logging_config import configure_logging

load_dotenv()

def create_app():
    """Initialize Flask app"""
    app = Flask(__name__)
    
    CORS(app)
    
    # Set up logging
    configure_logging(app)
    
    # AWS RDS PostgreSQL Configuration
    app.config['DATABASE'] = {
        'dbname': os.getenv('DATABASE_NAME'),
        'user': os.getenv('DATABASE_USER'),
        'password': os.getenv('DATABASE_PASSWORD'),
        'host': os.getenv('DATABASE_HOST'),
        'port': os.getenv('DATABASE_PORT'),
    }

    # Register Routes
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(movie_bp, url_prefix='/api')
    app.register_blueprint(todo_bp, url_prefix='/api')
    
    # Register Swagger UI
    SWAGGER_URL = '/api/docs'  # URL where Swagger UI will be accessible
    API_URL = '/static/openapi.json'  # URL for your OpenAPI JSON file (make sure it exists!)
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Yoll User Service API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    app.teardown_appcontext(close_db)

    return app