from flask import Blueprint, jsonify, request
from .models import *
from pydantic import BaseModel
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        user = UserRequestBody(email=data["email"], password=data["password"])
    except ValueError as e:
        error_messages = []
        for error in e.errors():
            msg = error["msg"].split(", ", 1)[1]
            error_messages.append(msg)
        if error_messages:
            return jsonify({'message': ', '.join(error_messages)}), 400

    return jsonify(user)
   

@auth_bp.route('/register', methods=['POST'])
def register():
    
    return
# Aquí puedes definir las rutas relacionadas con la autenticación