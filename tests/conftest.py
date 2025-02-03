import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from flask import Flask
from app.controllers.default_controller import default_bp
from app.controllers.movie_controller import movie_bp
from app.controllers.todo_controller import todo_bp
from app.controllers.user_controller import user_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    # Register your blueprints
    app.register_blueprint(default_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(user_bp)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client