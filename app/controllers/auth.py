from flask import Blueprint, jsonify, request
from ..models.models import *
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginRequestBody()  
    errors = schema.validate(request.json)
    if errors:
        return errors, 422
    else:
        user_dict = LoginRequestBody().load(request.json)
        password = user_dict["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        new_user = User(username=user_dict["email"],password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

@auth_bp.route('/register', methods=['POST'])
def register():
    
    return
# Aquí puedes definir las rutas relacionadas con la autenticación