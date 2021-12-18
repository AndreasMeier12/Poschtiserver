import copy
from typing import Dict, List

from .datatypes import ShoppingItem, Command, ListCommand, ShoppingList, CommandType


def merge(client, server):


    commands = sorted(client + server)
    res = {}
    for command in commands:
        handle(command, res)
    return [x for x in res.values()]




def handle(command: Command, res):
    if command.type == CommandType.UPDATE:
        handle_update(command, res)
    if command.type == CommandType.CREATE:
        handle_create(command, res)
    if command.type == CommandType.DELETE:
        handle_delete(command, res)


def handle_create( a: Command, res: dict):

    asdf = copy.copy(a.get_item())
    res[asdf.id] = asdf


def handle_update(a: Command, res: dict):
    asdf: ShoppingItem = copy.copy(a.get_item())
    res[asdf.id] = asdf


def handle_delete(a: Command, res):
        del res[a.get_id()]

def merge_lists(lists: List[ListCommand]):
    res: Dict[int, ShoppingList] = {}
    asdf = sorted(lists, key=lambda x: x.timestamp)
    for a in asdf:
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
        del res[a.item.id]
