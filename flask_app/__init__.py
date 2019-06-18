from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mail import Mail

from flask_app.routes import apply_routes


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    CORS(app, resources={r"/api/*": {"origins": r"williamcabell.me/*"}})

    return app


if __name__ == "__main__":
    app.run()
