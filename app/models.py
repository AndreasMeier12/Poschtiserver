from sqlalchemy import ForeignKey

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))






class ListCommandModel(db.Model):
    command_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'),  nullable=False, primary_key=True)
    list_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    origin = db.Column(db.String, nullable=False, default='server')

