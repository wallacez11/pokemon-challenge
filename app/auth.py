from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return
# Aquí puedes definir las rutas relacionadas con la autenticación