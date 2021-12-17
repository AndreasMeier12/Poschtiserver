from typing import Dict, List

from .datatypes import ShoppingItem, Command, Create, Delete, Update, ListCommand, ShoppingList
import copy



def merge(client, server):
    client_ids = {}
    server_ids = {}

    commands = sorted(client + server)
    res = {}
    for command in commands:
        handle(command, res, client_ids, server_ids)
    return sorted([x for x in res.values()], key=lambda x: x.id)



def find_max_id(client_ids: dict, server_ids: dict):
    if len(server_ids) == 0 and len(client_ids) == 0:
        return 0

    if len(server_ids)  == 0:
        return max(client_ids.values())
    if len(client_ids) == 0:
        return max(server_ids.values())

    return max( max( client_ids.values() ), max(server_ids.values()))

def handle(command: Command, res, client_ids, server_ids):
    if isinstance(command, Update):
        handle_update(command, res, client_ids, server_ids)
    if isinstance(command, Create):
        handle_create(command, res, client_ids, server_ids)
    if isinstance(command, Delete):
        handle_delete(command, res, client_ids, server_ids)


def handle_create( a: Create, res: dict, client_ids: dict, server_ids: dict ):
    max_id = find_max_id(client_ids, server_ids)
    cur_id = max_id + 1
    if a.get_origin() == 'server':
        server_ids[a.get_id()] = cur_id
    if a.get_origin() == 'client':
        client_ids[a.get_id()] = cur_id
    asdf = copy.copy(a.get_item())
    asdf.id = cur_id
    res[cur_id] = asdf


def handle_update(a: Update, res: dict, client_ids, server_ids):
    asdf: ShoppingItem = copy.copy(a.get_item())
    if a.get_origin() == 'server':
        asdf.id = server_ids[a.get_id()]
    else:
        asdf.id = client_ids[a.get_id()]
    res[asdf.id] = asdf


def handle_delete(a: Delete, res, client_ids: dict, server_ids: dict):
    if a.get_origin() == 'server':
        del res[server_ids[a.get_id()]]
    else:
        del res[client_ids[a.get_id()]]

def merge_lists(lists: List[ListCommand]):
    res: Dict[int, ShoppingList] = {}
    server_ids: Dict[int, int] = {}
    client_ids: Dict[int, int] = {}
    asdf = sorted(lists, key=lambda x: x.timestamp)
    for a in asdf:
        handle_list_command(a, res, server_ids, client_ids)
    return sorted([x for x in res.values()], key=lambda x: x.id)


def handle_list_command(a: ListCommand, res: Dict[int, ShoppingList], server_ids: dict, client_ids: dict):
    if a.type == 'create':
        create_list(a, res, server_ids, client_ids)
    if a.type == 'delete':
        delete_list(a, res, server_ids, client_ids)



def create_list(a: ListCommand, res: Dict[int, ShoppingList], server_ids: dict, client_ids: dict):
    cur_id = max([x for x in res.keys() ], default=0) + 1
    if a.origin == 'server':
        server_ids[a.item.id] = cur_id
    if a.origin == 'client':
        client_ids[a.item.id] = cur_id
    res[cur_id] = ShoppingList(cur_id, a.item.name)

def delete_list(a: ListCommand, res: Dict[int, ShoppingList], server_ids: dict, client_ids: dict):
    if a.origin == 'server':
        del res[server_ids[a.item.id]]
    if a.origin == 'client':
        del res[client_ids[a.item.id]]