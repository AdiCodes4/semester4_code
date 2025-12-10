from datetime import datetime, timezone
from flask import current_app
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, Email, Regexp, OneOf
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from config import Config

from app.extensions import db


class UserIn(Schema):
    name = String(required=True, validate=Length(min=0, max=32))
    email = String(required=True, validate=Email())
    password = String(
        required=True,
        load_only=True,
        validate=[
            Length(min=8, max=24),
            Regexp(
                r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@#$%^&+=!]{8,}$',
                error="Password must contain letters and numbers."
            )
        ]
    )


class UserOut(Schema):
    id = String()
    name = String()
    email = String()
    password = String()


class LoginIn(Schema):
    email = String(required=True)
    password = String(required=True)


class TokenOut(Schema):
    token = String()
    duration = Integer()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password  # ← nutzt den setter automatisch

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def generate_auth_token(self, expires_in=600):
        exp_timestamp = int(datetime.now(timezone.utc).timestamp()) + expires_in
        return encode(
            {'id': self.id, 'exp': exp_timestamp},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
