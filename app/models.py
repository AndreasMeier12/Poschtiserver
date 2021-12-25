import datetime
import logging
from typing import Optional

import jwt
from sqlalchemy import ForeignKey

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from argon2 import PasswordHasher

from app import db, login, app

ph = PasswordHasher()
TOKEN_TTL_DAYS = 2

class User(UserMixin, db.Model):
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        verified = ph.verify(self.password_hash, password)
        if verified and ph.check_needs_rehash(self.password_hash):
            self.set_password(password)
        return verified

    #https://realpython.com/token-based-authentication-with-flask/
    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=TOKEN_TTL_DAYS),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    #https://realpython.com/token-based-authentication-with-flask/
    @staticmethod
    def decode_auth_token(auth_token) -> Optional[str]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            logging.log(logging.INFO, "Token expired")
        except jwt.InvalidTokenError:
            logging.log(logging.INFO, "Token invalid")
        return None


@login.user_loader
def load_user(id):
    return User.query.get(id)






class ListCommandModel(db.Model):
    command_id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), ForeignKey('user.id'),  nullable=False, primary_key=True)
    list_id = db.Column(db.String(40))
    type = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    origin = db.Column(db.String(10), nullable=False, default='server')
    name = db.Column(db.String(100))

class ItemCommandModel(db.Model):
    command_id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), ForeignKey('user.id'), primary_key=True)
    list_id = db.Column(db.String(40))
    item_id = db.Column(db.String(40))

    type = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    origin = db.Column(db.String(10), nullable=False, default='server')
    name = db.Column(db.String(100))
    quantity = db.Column(db.String(100))
    shop = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)
