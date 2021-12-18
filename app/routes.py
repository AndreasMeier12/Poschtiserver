import datetime
import json
import re
from app.utils import get_uuid_str as uuid

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user, login_user
from sqlalchemy import func
from werkzeug.security import check_password_hash

from app import app, db
from app.business.datatypes import ShoppingList, CommandType
from app.business.merge import merge_lists
from app.forms import AddListForm
from app.models import User, ListCommandModel
from app.utils import get_next_list_command_id, model_to_internal_list_command


@app.route('/index')
@app.route('/')
def index():
    return render_template('static/html/base.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if not re.match('[^@]+@[^@]+\.[^@]+', username):
            error = 'Name does not seem to be an e-mail address'
        existing = User.query.filter_by(username=username).first()
        if existing:
            error = 'please choose another user name, if you have already register recover your password'

        if error:
            flash(error)
        else:
            user: User = User(username=username, id=str(uuid.uuid1()))
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template('static/html/auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = True
        elif not user.check_password(password):
            error = True

        if not error:
            login_user(user)
        else:
            flash('Login information not correct')

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


@app.route('/lists', methods=('GET', 'POST', 'DELETE'))
@login_required
def lists():
    form = AddListForm()
    user_id = current_user.id
    time = datetime.datetime.now()
    if request.method == 'POST':
        name = form.data['list_name']
        new_id = str(uuid())
        origin='server'
        list_id = str(uuid())
        command = ListCommandModel(command_id=new_id, list_id=list_id, origin=origin, user_id=user_id, type=CommandType.CREATE, timestamp=time, name=name)
        db.session.add(command)
        db.session.commit()
        listcommand: ListCommandModel = ListCommandModel()
    if request.method == 'DELETE':
        data = json.loads(request.data)
        origin = data['origin']
        list_id = data['id']
        new_id = uuid()
        command = ListCommandModel(command_id=new_id, list_id=list_id, origin=origin, user_id=user_id, type=CommandType.DELETE, timestamp=time)
        db.session.add(command)
        db.session.commit()

    lists_raw = db.session.query(ListCommandModel).filter(ListCommandModel.user_id == user_id).all()
    lists = [model_to_internal_list_command(x) for x in lists_raw]
    merged = merge_lists(lists)
    return render_template('static/html/lists.html', form=form, lists=merged)


@app.route('/list')
@login_required
def single_list():
    return render_template('static/html/list.html')


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
