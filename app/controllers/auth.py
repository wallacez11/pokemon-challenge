from flask import Blueprint, request, jsonify
from flask_login import  login_user, logout_user
from ..models.models import *
from sqlalchemy.exc import IntegrityError
import bcrypt

auth_bp = Blueprint('auth', __name__)




@auth_bp.route('/auth/register', methods=['POST'])
def register():
    schema = LoginRequestBody()  
    errors = schema.validate(request.json)
    if errors:
        return errors, 422
    else:
        user_dict = RegisterRequestBody().load(request.json)
        password = user_dict["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        new_user = User(username=user_dict["email"],password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created'}) , 201
        except IntegrityError  as e:
            db.session.rollback()
            if 'UNIQUE constraint failed: user.username' in str(e):
                return jsonify({'message': 'Username already exists'}), 409 
            else:
                return str(e), 500  

        

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    schema = LoginRequestBody()  
    errors = schema.validate(request.json)
    if errors:
        return errors, 422
    else:
        user_dict = LoginRequestBody().load(request.json)
        user = User.query.filter_by(username=user_dict["email"]).first()
        
   
        body_password = user_dict["password"]
       
        if user:
            if bcrypt.checkpw(body_password.encode('utf-8'),user.password_hash):
                login_user(user)
                return jsonify({'message': 'Successfully logged in'}), 200
            else:
                return jsonify({'message': 'Email or Password Incorrect'}), 401, 
        else:
            return 'User not Found', 404
    
    
@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

   
