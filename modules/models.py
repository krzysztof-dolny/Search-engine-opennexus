from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    password = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('temporary_passwords', lazy=True))
