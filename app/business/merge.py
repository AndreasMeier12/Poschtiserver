import copy
from typing import Dict, List
from collections import OrderedDict

from .datatypes import ShoppingItem, Command, ListCommand, ShoppingList, CommandType


def merge(client, server=None):
    if server is None:
        server = []

    commands = sorted(client + server)
    res = OrderedDict()
    for command in commands:
        handle(command, res)
    return [x for x in res.values()]




def handle(command: Command, res):
    if command.type is CommandType.UPDATE:
        handle_update(command, res)
    if command.type is CommandType.CREATE:
        handle_create(command, res)
    if command.type is CommandType.DELETE:
        handle_delete(command, res)


def handle_create( a: Command, res: dict):

    b = copy.copy(a.get_item())
    res[b.id] = b


def handle_update(a: Command, res: dict):
    b: ShoppingItem = copy.copy(a.get_item())
    res[b.id] = b


def handle_delete(a: Command, res):
    if a.item.id in res:
        del res[a.get_id()]

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

