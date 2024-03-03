from flask import Blueprint, request, jsonify, current_app
from flask_login import  login_user, logout_user
from ..models.models import *
from sqlalchemy.exc import IntegrityError
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])

def register():
    schema = RegisterRequestBody()  
    errors = schema.validate(request.json)
    if errors:
        current_app.logger.warning(f'Invalid registration attempt: {errors}')
        return errors, 422
    else:
        user_dict = RegisterRequestBody().load(request.json)
        password = user_dict["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        new_user = User(username=user_dict["email"],password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            current_app.logger.info('User registered successfully.')
            return jsonify({'message': 'User created'}), 201
        except IntegrityError  as e:
            db.session.rollback()
            if 'UNIQUE constraint failed: user.username' in str(e):
                current_app.logger.warning('Registration attempt with existing email.')
                return jsonify({'message': 'Username already exists'}), 409 
            else:
                current_app.logger.error(f'Error while trying to register user: {str(e)}')
                return str(e), 500  

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    schema = LoginRequestBody()  
    errors = schema.validate(request.json)
    if errors:
        current_app.logger.warning(f'Invalid login attempt: {errors}')
        return errors, 422
    else:
        user_dict = LoginRequestBody().load(request.json)
        user = User.query.filter_by(username=user_dict["email"]).first()

        body_password = user_dict["password"]

        if user:
            if bcrypt.checkpw(body_password.encode('utf-8'), user.password_hash):
                current_app.logger.info(f'User {user.username} logged in successfully.')
                login_user(user)
                return jsonify({'message': 'Successfully logged in'}), 200
            else:
                current_app.logger.warning('Login attempt with incorrect email or password.')
                return jsonify({'message': 'Email or Password Incorrect'}), 401
        else:
            current_app.logger.warning('User not found.')
            return 'User not Found', 404

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    logout_user()
    current_app.logger.info('User logged out successfully.')
    return jsonify({'message': 'Logged out successfully'}), 200

   
