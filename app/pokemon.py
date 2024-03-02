from flask import Blueprint, jsonify

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/pokemon/type/<name>')
def get_pokemon_type_by_name(name):
    return 