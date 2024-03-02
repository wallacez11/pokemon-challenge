from flask import Flask
from .config import Config

from app.controllers.pokemon import pokemon_bp
from app.controllers.auth import auth_bp
from .utils import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(pokemon_bp)
    app.register_blueprint(auth_bp)

    return app