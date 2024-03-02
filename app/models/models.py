from flask_login import UserMixin
from ..utils import db
from marshmallow import Schema, fields, ValidationError, validate



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class RegisterRequestBody(Schema):
    email = fields.Email()
    password = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$',
            error='Password must have at least 8 characters, one uppercase letter, one lowercase letter, and one digit.'
        )
    )
class LoginRequestBody(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True
    )