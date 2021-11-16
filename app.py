from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from . import create_app
from model import User

app = create_app()
db = SQLAlchemy(app)

@app.route('/')
def main():
    new_User = User()
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
