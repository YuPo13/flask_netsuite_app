from flask import Flask
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.api_key

    with app.app_context():
        return app
