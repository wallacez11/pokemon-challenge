from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .pokemon import pokemon_bp
    from .auth import auth_bp

    app.register_blueprint(pokemon_bp)
    app.register_blueprint(auth_bp)

    return app