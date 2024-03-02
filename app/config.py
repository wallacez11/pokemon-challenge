import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    POKEMON_API_BASE_URL = os.environ.get('POKEMON_API_BASE_URL')
    OPEN_METEO_API_BASE_URL = os.environ.get('OPEN_METEO_API_BASE_URL')