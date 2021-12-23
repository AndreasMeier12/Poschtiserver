import datetime
import json

from sqlalchemy.engine import Row
from uuid import uuid4

from app.business import datatypes
from app.business.datatypes import ListCommand, ShoppingList, ShoppingItem, \
    Command, CommandType
from app.models import ListCommandModel, ItemCommandModel, User


def get_next_list_command_id(a: Row) -> int:
    if len(a) == 1 and a[0] is None:
        return 1
    return a[0] + 1

def model_to_internal_list_command(a: ListCommandModel) -> ListCommand:
    payload = ShoppingList(a.list_id, a.name)
    return ListCommand(origin=a.origin, type=datatypes.CommandType.get_by_id(a.type), timestamp=a.timestamp, item=payload)


def model_to_internal_item_command(a: ItemCommandModel) -> Command:
    doneness = True if a.done else False
    payload = ShoppingItem(a.name, a.quantity, a.shop, a.item_id, a.list_id, done=doneness)
    return Command(payload, a.timestamp, a.origin, datatypes.CommandType.get_by_id(a.type))


def get_uuid_str() -> str:
    return str(uuid4())

def item_commands_from_json(a: str, user: User):
    dict = json.loads(a)
    item: ShoppingItem =ShoppingItem(dict['name'], dict['quantity'], dict['shop'], dict['itemKey'], dict['shoppingList'], dict['done'])
    #item, datetime.datetime.fromtimestamp(dict['timestamp']/1e3), 'server', CommandType.get_by_name(dict['type']
    return ItemCommandModel(command_id = dict['commandKey'], user_id = user.id, list_id = dict['shoppingList'], item_id = dict['itemKey'], type = CommandType.get_by_name(dict['type']), timestamp=datetime.datetime.fromtimestamp(dict['timestamp']/1e3), origin='client', name=dict['name'], quantity=dict['quantity'], shop=dict['shop'], done=dict['done'] )

def list_commands_from_json(a: str, user: User):
    dict = json.loads(a)
    list = ShoppingList(dict['listKey'], dict['name'])
    return ListCommandModel(command_id=dict["commandKey"], name=dict['name'], list_id=dict['listKey'], origin='client', user_id=user.id, type=CommandType.get_by_name(dict['type']), timestamp=datetime.datetime.fromtimestamp(dict['timestamp']/1e3))