import datetime
import logging
from typing import Optional

import jwt
from sqlalchemy import ForeignKey

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from argon2 import PasswordHasher

import config
from app import db, login, app

ph = PasswordHasher()
TOKEN_TTL_DAYS = 2

class User(UserMixin, db.Model):
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    settings = db.relationship('UserSettings', backref='user' , lazy=True)

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
    def encode_auth_token(self, validity_in_hours:int) -> (bytes, datetime, datetime):
        """
        Generates the Auth Token
        :return: string
        """
        exp = datetime.datetime.utcnow() + datetime.timedelta(
            hours=validity_in_hours)
        iat = datetime.datetime.utcnow()
        try:
            payload = {
                'exp': exp,
                'iat': iat,
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            ), exp, iat
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

class UserSettings(db.Model):
    user_id = db.Column(db.String(40), ForeignKey('user.id'),  nullable=False, primary_key=True)
    token_duration = db.Column(db.Integer, nullable=True)
    last_issued_token = db.Column(db.DateTime, nullable=True, default=None)
    last_issued_expiration = db.Column(db.DateTime, nullable=True, default=None)
    delete_confirmation = db.Column(db.String, nullable=True, default=None)

    def __init__(self, user: User, token_duration: int=None ):
        self.user_id = user.id
        if token_duration is None:
            token_duration = config.Config.TOKEN_VALIDITY_DURATION_HOURS
        self.token_duration = token_duration

    def set_token_validity(self, token_duration: int):
        self.token_duration = token_duration


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


class UpdateField(db.Model):
    command_id = db.Column(db.String(40), ForeignKey("item_command_model.command_id"), primary_key=True)
    uuid = db.Column(db.String(40), primary_key=True)
    field = db.Column(db.String(20), nullable=False)
    command = db.relationship("ItemCommandModel", back_populates="fields")

    def __init__(self, command_id:str, field:str, uuid:str):
        self.command_id = command_id
        self.field = field
        self.uuid = uuid




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
    fields = db.relationship('UpdateField')