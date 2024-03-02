import os

class Config:
    SECRET_KEY = 'sua_chave_secreta_aqui'
    POKEMON_API_BASE_URL = os.environ.get('POKEMON_API_BASE_URL')
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    