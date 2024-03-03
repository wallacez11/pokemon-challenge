import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    POKEMON_API_BASE_URL = "https://pokeapi.co/api/v2/"
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    