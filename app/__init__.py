import os
from flask import Flask
from app.controllers.user_controller import user_bp
from app.db import close_db 
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Initialize Flask app"""
    app = Flask(__name__)

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

    app.teardown_appcontext(close_db)

    return app