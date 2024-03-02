from flask_login import UserMixin
from .utils import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)