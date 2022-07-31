import datetime
import json

from sqlalchemy.engine import Row
from uuid import uuid4

from app.business import datatypes
from app.business.datatypes import ListCommand, ShoppingList, ShoppingItem, \
    Command, CommandType, UpdateFieldType
from app.models import ListCommandModel, ItemCommandModel, User, UpdateField


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
    return Command(payload, a.timestamp, a.origin, datatypes.CommandType.get_by_id(a.type), fields=[x.field for x in a.fields])


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

def make_ordinal(n): # Florian Brucker https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def get_num_for_delete_phrase(a: str) -> int:
    if len(a) < 20:
        return 2
    return len(a) // 10

def get_delete_phrase(a: str, num: int) -> str:
    b = ''.join([x for x in a if x.isalnum()])
    return b[::num]