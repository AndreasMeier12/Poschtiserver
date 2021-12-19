import datetime
import json
import re
from app.utils import get_uuid_str as uuid, model_to_internal_item_command, get_uuid_str

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user, login_user
from sqlalchemy import func
from werkzeug.security import check_password_hash

from app import app, db
from app.business.datatypes import ShoppingList, CommandType
from app.business.merge import merge_lists, merge
from app.forms import AddListForm, AddItemForm
from app.models import User, ListCommandModel, ItemCommandModel
from app.utils import get_next_list_command_id, model_to_internal_list_command


@app.route('/index')
@app.route('/')
def index():
    return render_template('base.html')


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
            user: User = User(username=username, id=str(uuid()))
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template('auth/register.html')


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

    return render_template('auth/login.html')


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
        new_id = get_uuid_str()
        origin='server'
        list_id = get_uuid_str()
        command = ListCommandModel(command_id=new_id, list_id=list_id, origin=origin, user_id=user_id, type=CommandType.CREATE.value, timestamp=time, name=name)
        db.session.add(command)
        db.session.commit()
        listcommand: ListCommandModel = ListCommandModel()
    if request.method == 'DELETE':
        data = json.loads(request.data)
        origin = data['origin']
        list_id = data['id']
        new_id = uuid()
        command = ListCommandModel(command_id=new_id, list_id=list_id, origin=origin, user_id=user_id, type=CommandType.DELETE.value, timestamp=time)
        db.session.add(command)
        db.session.commit()

    lists_raw = db.session.query(ListCommandModel).filter(ListCommandModel.user_id == user_id).all()
    lists = [model_to_internal_list_command(x) for x in lists_raw]
    merged = merge_lists(lists)
    return render_template('lists.html', form=form, lists=merged)


@app.route('/list/<list_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@login_required
def single_list(list_id):
    form = AddItemForm()
    user_id = current_user.id
    time = datetime.datetime.now()




    if request.method == 'POST':
        item = form.data['item']
        shop = form.data['shop']
        quantity = form.data['quantity']

        command = ItemCommandModel(command_id=uuid(), user_id=user_id, item_id=uuid(), list_id=list_id, type=CommandType.CREATE.value, timestamp=time,
                                   name=item, quantity=quantity, shop=shop)
        db.session.add(command)
        db.session.commit()
        pass
    if request.method == 'PATCH':
        data = json.loads(request.data)
        command = ItemCommandModel(command_id=get_uuid_str(), user_id = user_id, item_id=data['id'], list_id=list_id, type=CommandType.UPDATE.value, timestamp=time, name=data['name'], shop=data['shop'], quantity=data['quantity'], done=data['done'])
        db.session.add(command)
        db.session.commit()
    if request.method == 'DELETE':
        data = json.loads(request.data)
        command = ItemCommandModel(command_id=get_uuid_str(), user_id = user_id, item_id=data['id'], list_id=list_id, type=CommandType.DELETE.value, timestamp=time)
        db.session.add(command)
        db.session.commit()

    items_raw = db.session.query(ItemCommandModel).filter(ItemCommandModel.user_id == user_id, ItemCommandModel.list_id == list_id).all()
    items = [model_to_internal_item_command(x) for x in items_raw]
    merged = merge(items)



    return render_template('list.html', form=form, list_id=list_id, items=merged)


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
