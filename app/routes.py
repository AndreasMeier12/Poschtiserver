import json

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required
from werkzeug.security import check_password_hash

from app import app
from app.models import User


@app.route('/index')
@app.route('/')
def index():
    return render_template('static/html/base.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        return redirect(url_for("auth.login"))

    return render_template('static/html/auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query(username=username).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)

    return render_template('static/html/auth/login.html')


def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        User.query.get(int(user_id))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/lists')
@login_required
def show_lists():
    return render_template('../templates/static/html/lists.html')


@app.route('/list')
@login_required
def show_single_lists():
    return render_template('../templates/static/html/list.html')


@app.route('/lists/api', methods=['GET'])
@login_required
def get_lists():
    user = session.get('user_id')
    return "asdf"


@app.route('/lists/api', methods=['POST'])
@login_required
def handle_list_update():
    user = session.get('user_id')
    a = json.loads(request.data)
    return "fdsa"
