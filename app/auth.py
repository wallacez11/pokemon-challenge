from flask import Blueprint, jsonify, request
from .models import *
from pydantic import BaseModel
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print(jsonify(data))
    return jsonify(data)
   

@auth_bp.route('/register', methods=['POST'])
def register():
    
    return
# Aquí puedes definir las rutas relacionadas con la autenticación