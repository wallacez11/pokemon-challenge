import logging
from logging.handlers import RotatingFileHandler
import os

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
    configure_logger(app)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.login_message = "User needs to be logged in to view this page"
    login_manager.init_app(app)
   

    @login_manager.user_loader
    def user_loader(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user
        return None
    
    db.init_app(app)
    app.register_blueprint(pokemon_bp)
    app.register_blueprint(auth_bp)

    return app

##logging configuration
def configure_logger(app):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    basedir = os.path.abspath(os.path.dirname(__file__))
    logs_dir = os.path.join(basedir, 'logs')

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
  
    file_handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), maxBytes=10240, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

