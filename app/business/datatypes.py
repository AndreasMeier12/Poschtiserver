from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC
from datetime import datetime

@dataclass
class CommandType:
    CREATE = 1
    UPDATE = 2
    DELETE = 3

    @staticmethod
    def get_by_name(a: str) -> int:
        if a=='CREATE':
            return CommandType.CREATE
        if a=='UPDATE':
            return CommandType.UPDATE
        if a=='DELETE':
            return CommandType.DELETE

    @staticmethod
    def get_by_id(a: int) -> str:
        if a==CommandType.CREATE:
            return 'CREATE'
        if a==CommandType.UPDATE:
            return 'UPDATE'
        if a==CommandType.DELETE:
            return 'DELETE'


@dataclass
class Log:
    pass

@dataclass
class ShoppingItem:
    name: str
    quantity: str
    shop: str
    id: int
    list_id: int

def get_command(id: int, list_id: int, name: str, shop: str, quantity: str, timestamp: datetime, type: 'str', origin: str):
    item : ShoppingItem = ShoppingItem(name, quantity, shop, id, list_id)
    if type == 'update':
        return Update(item, timestamp, origin)
    if type == 'create':
        return Create(item, timestamp, origin)
    if type == 'delete':
        return Delete(item, timestamp, origin)

class Command(ABC):
    def get_timestamp(self):
        pass

    def __lt__(self, other):
        return self.get_timestamp() < other.get_timestamp()

    def get_origin(self):
        pass

    def get_id(self):
        pass
    def get_item(self):
        pass


class Update(Command):
    def __init__(self, item: ShoppingItem, timestamp: datetime, origin: str):
        self.item: ShoppingItem = item
        self.timestamp: datetime = timestamp
        self.origin = origin

    def get_item(self) -> ShoppingItem:
        return self.item

    def get_origin(self):
        return self.origin

    def get_id(self):
        return self.item.id

    def get_timestamp(self):
        return self.timestamp

class Create(Command):
    def __init__(self, item: ShoppingItem, timestamp: datetime, origin: str):
        self.item : ShoppingItem = item
        self.timestamp: datetime = timestamp
        self.origin = origin

    def get_item(self) -> ShoppingItem:
        return self.item

    def get_timestamp(self):
        return self.timestamp

    def get_origin(self):
        return self.origin

    def get_id(self):
        return self.item.id

class Delete(Command):
    def __init__(self, item: ShoppingItem, timestamp: datetime, origin: str):
        self.item : ShoppingItem = item
        self.timestamp: datetime = timestamp
        self.origin = origin

    def get_item(self) -> ShoppingItem:
        return self.item

    def get_timestamp(self):
        return self.timestamp

    def get_origin(self):
        return self.origin

    def get_id(self):
        return self.item.id

@dataclass()
class ShoppingList:
    id: int
    name: str

@dataclass
class ListCommand():
    origin: str
    type: str
    item: ShoppingList
    timestamp: datetime

@dataclass()
class ShoppingList():
    id: int
    name: str

