import enum
import sys, os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from create_app import db

class UserType(enum.Enum):
    ADMIN = "admin"
    GENERAL = "general"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    projects =  db.relationship('Project', backref='user', lazy='dynamic')  # option 1
    user_type = db.Column(db.Enum(UserType))

    def __repr__(self):
        return '<User {}, password {}>'.format(self.email, self.password)

    def get_hash_password(password):
        """Create hashed password."""
        return generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    dir = db.Column(db.String(80), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('projects', lazy=True))  # option 2