import datetime
import json
import logging
import re
from typing import Optional

from flask import (
    flash, g, redirect, render_template, request, session, url_for, abort
)
from flask_login import login_required, current_user, login_user
from sqlalchemy import delete

from app import app, db
from app import csrf
from app.business.datatypes import CommandType
from app.business.merge import merge_lists, merge
from app.forms import AddListForm, AddItemForm, TokenValidityForm, \
    DeleteAccountForm
from app.models import User, ListCommandModel, ItemCommandModel, UserSettings
from app.utils import get_uuid_str as uuid, model_to_internal_item_command, \
    get_uuid_str, list_commands_from_json, item_commands_from_json, \
    get_num_for_delete_phrase, get_delete_phrase, make_ordinal
from app.utils import model_to_internal_list_command


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
            settings: UserSettings = UserSettings(user)
            user.set_password(password)
            db.session.add(settings)
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
            if 'stayloggedin' in request.form:
                session.permanent = True
            return redirect(url_for('lists'))
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
    user_id = current_user.id
    time = datetime.datetime.now()

    if request.method == 'POST':
        form = AddItemForm()
        item = form.data['item']
        shop = form.data['shop']
        quantity = form.data['quantity']

        command = ItemCommandModel(command_id=uuid(), user_id=user_id, item_id=uuid(), list_id=list_id, type=CommandType.CREATE.value, timestamp=time,
                                   name=item, quantity=quantity, shop=shop)
        db.session.add(command)
        db.session.commit()
    if request.method == 'PATCH':
        data = json.loads(request.data)
        command = ItemCommandModel(command_id=get_uuid_str(), user_id = user_id, item_id=data['id'], list_id=list_id, type=CommandType.UPDATE.value, timestamp=time, name=data['name'], shop=data['shop'], quantity=data['quantity'], done=data['done'])
        db.session.add(command)
        db.session.commit()

    if request.method == 'DELETE':
        data = json.loads(request.data)
        for x in data:
            command = ItemCommandModel(command_id=get_uuid_str(), user_id = user_id, item_id=x, list_id=list_id, type=CommandType.DELETE.value, timestamp=time)
            db.session.add(command)
        db.session.commit()


    items_raw = db.session.query(ItemCommandModel).filter(ItemCommandModel.user_id == user_id, ItemCommandModel.list_id == list_id).all()
    items = [model_to_internal_item_command(x) for x in items_raw]
    merged = merge(items)
    form = AddItemForm()
    return render_template('list.html', form=form, list_id=list_id, items=sorted(merged, key=lambda x: x.shop))


@app.route('/api/list', methods=['POST'])
@csrf.exempt
def get_lists():
    d = json.loads(request.data)
    token = d['token']
    user = authenticate_via_token(token)
    if user is None:
        abort(401)
    return getData(user)


@csrf.exempt
@app.route('/api/list', methods=['PUT', 'PATCH'])
def handle_list_update():

    d = json.loads(request.data)
    token = d['token']
    user = authenticate_via_token(token)
    if user is None:
        abort(401)

    lists = d['lists']
    items = d['items']
    item_commands = [item_commands_from_json(x, user) for x in items]
    list_commands = [list_commands_from_json(x, user) for x in lists]
    if request.method == 'POST':
        statement = delete(ListCommandModel).where(ListCommandModel.user_id == user.id)
        statement2 = delete(ItemCommandModel).where(ItemCommandModel.user_id == user.id)
        db.engine.execute(statement)
        db.engine.execute(statement2)
    command_ids = [x.command_id for x in item_commands]

    clashing_ids = {x[0] for x in db.session.query(ItemCommandModel.command_id).filter(ItemCommandModel.command_id.in_(command_ids)).all()}

    db.session.bulk_save_objects([x for x in item_commands if x.command_id not in clashing_ids])
    db.session.bulk_save_objects(list_commands)
    db.session.commit()



    return getData(user)

def getData(user: User):
    list_commands_raw = db.session.query(ListCommandModel).filter(ListCommandModel.user_id == user.id).all()
    item_commands_raw = db.session.query(ItemCommandModel).filter(ListCommandModel.user_id == user.id).all()
    list_commands = [model_to_internal_list_command(x) for x in list_commands_raw]
    item_commands = [model_to_internal_item_command(x) for x in item_commands_raw]
    lists = merge_lists(list_commands)
    items = merge(item_commands)
    vals = {'lists': lists, 'items': items}

    return vals


@login_required
@app.route('/token', methods=['GET'])
def token():
    settings: UserSettings = db.session.query(UserSettings).filter(UserSettings.user_id==current_user.id).first()
    return render_template('auth/token.html', settings=settings)

@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    token_validity_form = TokenValidityForm()

    return render_template('auth/settings.html',
                           token_validity_form=token_validity_form)

@login_required
@app.route('/api/token/set', methods=['POST'])
def set_token():
    token_validity_form = TokenValidityForm()
    user_id = current_user.id
    settings: UserSettings = db.session.query(UserSettings).filter(UserSettings.user_id==user_id).first()
    settings.token_duration = token_validity_form.data['token_validity_field']
    db.session.add(settings)
    db.session.commit()


    return redirect(url_for('settings'))


@login_required
@app.route('/api/token', methods=['GET'])
def get_token():
    settings: UserSettings = db.session.query(UserSettings).filter(
        UserSettings.user_id == current_user.id).first()

    token, exp, iat = current_user.encode_auth_token(settings.token_duration)
    settings.last_issued_token  = iat
    settings.last_issued_expiration  = exp
    db.session.add(settings)
    db.session.commit()

    return {'val': token.decode('utf-8'), 'iat': iat, 'exp': exp}

def authenticate_via_token(token: str) -> Optional[User]:
    user_id = User.decode_auth_token(token.strip().encode())
    if not user_id:
        return None
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None
    return user

@login_required
@app.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    settings: UserSettings = db.session.query(UserSettings).filter(
        UserSettings.user_id == current_user.id).first()
    form = DeleteAccountForm()
    if request.method == 'POST':
        confirmation_phrase = form.data['confirmation']
        if confirmation_phrase == settings.delete_confirmation:
            db.session.delete(current_user)
            db.session.delete(settings)

            db.session.commit()
            session.clear()
            return redirect('/')
    phrase = 'The flames will rise'
    num = get_num_for_delete_phrase(phrase)
    settings.delete_confirmation = get_delete_phrase(phrase, num)
    db.session.add(settings)
    db.session.commit()
    return render_template('auth/delete_account.html', num=make_ordinal(num), phrase=phrase, form=form)
