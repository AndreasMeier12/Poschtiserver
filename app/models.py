from sqlalchemy import ForeignKey

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from argon2 import PasswordHasher

from app import db, login

ph = PasswordHasher()

class User(UserMixin, db.Model):
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        return ph.verify(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(id)






class ListCommandModel(db.Model):
    command_id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), ForeignKey('user.id'),  nullable=False, primary_key=True)
    list_id = db.Column(db.String(40))
    type = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    origin = db.Column(db.String, nullable=False, default='server')
    name = db.Column(db.String(100))

class ItemCommandModel(db.Model):
    command_id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), ForeignKey('user.id'), primary_key=True)
    list_id = db.Column(db.String(40))
    item_id = db.Column(db.String(40))

    type = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    origin = db.Column(db.String, nullable=False, default='server')
    name = db.Column(db.String(100))
    quantity = db.Column(db.String(100))
    shop = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)
