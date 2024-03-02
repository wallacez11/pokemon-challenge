from flask import Flask
from .config import Config
from flask_login import LoginManager

from app.controllers.pokemon import pokemon_bp
from app.controllers.auth import auth_bp
from .utils import db
from .models.models import User
import logging



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Esta função é usada para carregar o usuário com base no ID do usuário armazenado na sessão
        return User.query.get(int(user_id))

    db.init_app(app)

    app.register_blueprint(pokemon_bp)
    app.register_blueprint(auth_bp)

    return app
