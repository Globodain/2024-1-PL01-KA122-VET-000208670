from typing import Optional

import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login
import hashlib

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Ensure this field is always populated

    about_me = db.Column(db.String(140), nullable=True)
    last_seen = db.Column(db.DateTime, default=sa.func.now(), index=True)

    def avatar(self, size):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    def __repr__(self):
        return f'User: {self.username}'  # Use f-string for better readability

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=sa.func.now())

    author = so.relationship('User', backref='posts')  # Ensure the relationship is correctly defined

    def __repr__(self):
        return f'Post: {self.body}'  # Use f-string for better readability

        # I can't write shit in Python