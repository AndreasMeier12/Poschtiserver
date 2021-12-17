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
        if a.lower()=='create':
            return CommandType.CREATE
        if a.lower()=='update':
            return CommandType.UPDATE
        if a.lower()=='delete':
            return CommandType.DELETE

    @staticmethod
    def get_by_id(a: int) -> str:
        if a==CommandType.CREATE:
            return 'create'
        if a==CommandType.UPDATE:
            return 'update'
        if a==CommandType.DELETE:
            return 'delete'


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

class Command:
    def __init__(self, item: ShoppingItem, timestamp: datetime, origin: str, type: CommandType):
        self.item: ShoppingItem = item
        self.timestamp: datetime = timestamp
        self.origin = origin
        self.type = type


    def get_timestamp(self):
        pass

    def __lt__(self, other):
        return self.get_timestamp() < other.get_timestamp()

    def get_origin(self):
        return self.origin

    def get_id(self):
        return self.get_item().id

    def get_item(self) -> ShoppingItem:
        return self.item

    def get_type(self) -> CommandType:
        self.type

    def get_timestamp(self):
        return self.timestamp


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

