import copy
from collections import OrderedDict
from itertools import groupby
from typing import Dict, List, Optional

from .datatypes import ShoppingItem, Command, ListCommand, ShoppingList, \
    CommandType, UpdateFieldType


def merge(commands: List[Command]) -> List[ShoppingItem]:
    groups = {k: sorted(list(v)) for k, v in groupby(sorted(commands, key=lambda x: x.item.id), key=lambda x: x.item.id)}
    order = [x.item.id for x in sorted([y for y in commands if y.type.value == CommandType.CREATE.value])]
    return [res for x in order if (res:=handle_items(groups[x]))]

def handle_items(commands: List[Command]) -> Optional[ShoppingItem]:
    if any(x.type.value  == CommandType.DELETE.value for x in commands):
        return None
    ## find last command with field
    if len(commands) ==1:
        return commands[0].item
    strat = commands[0].item
    name: str = get_newest_update(commands, UpdateFieldType.NAME.value)
    shop: str = get_newest_update(commands, UpdateFieldType.SHOP.value)
    done: bool = get_newest_update(commands, UpdateFieldType.DONE.value)
    quantity: str = get_newest_update(commands, UpdateFieldType.QUANTITY.value)
    return ShoppingItem(name, quantity, shop, strat.id, strat.list_id, done)

def get_newest_update(commands: List[Command], field: str):
    updates = sorted(filter( lambda x: x.type==CommandType.UPDATE and field in x.fields, commands))
    if not updates:
        return vars(commands[0].item)[field]
    return vars(updates[-1].item)[field]


    return ShoppingItem()






def merge_lists(lists: List[ListCommand]):
    res: OrderedDict[int, ShoppingList] = OrderedDict()
    sorted_lists = sorted(lists, key=lambda x: x.timestamp)
    for a in sorted_lists:
        handle_list_command(a, res)
    return [x for x in res.values()]


def handle_list_command(a: ListCommand, res: Dict[int, ShoppingList]):
    if a.type is CommandType.CREATE:
        create_list(a, res)
    if a.type is CommandType.DELETE:
        delete_list(a, res)



def create_list(a: ListCommand, res: Dict[int, ShoppingList]):
    res[a.item.id] = ShoppingList(a.item.id, a.item.name)

def delete_list(a: ListCommand, res: Dict[int, ShoppingList]):
    if a.item.id in res:
        del res[a.item.id]

