from flask import Blueprint, jsonify
from flask_login import login_required
pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/app/pokemon',methods=['GET'])
@login_required
def get_pokemon_type_by_name():
    return jsonify({'message': 'rota protegida'}) , 201