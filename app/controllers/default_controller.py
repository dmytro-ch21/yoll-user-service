from flask import Blueprint, jsonify, request
import os
from dotenv import load_dotenv

default_bp = Blueprint("default", __name__)

load_dotenv()

DOCS_URL = os.getenv("DOCS_URL")


@default_bp.route("/")
def default_route():
    return jsonify(
        {
            "message": "Welcome to the Yoll Student API. Please refer to the OpenAPI documentation at the following URL:",
            "openapi_docs": DOCS_URL,
        }
    )
