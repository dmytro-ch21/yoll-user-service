import os
from flask import Flask
from app.routes import routes_bp
from app.db import close_db  # Import close_db() only
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('DATABASE_PASSWORD'))

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
    app.register_blueprint(routes_bp, url_prefix='/api')

    # Ensure database connections are closed after requests
    app.teardown_appcontext(close_db)

    return app