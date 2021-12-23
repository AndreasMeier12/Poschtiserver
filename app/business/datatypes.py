from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC
from datetime import datetime

@dataclass
class CommandType(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3

    @staticmethod
    def get_by_name(a: str):
        if a.lower()=='create':
            return CommandType.CREATE.value
        if a.lower()=='update':
            return CommandType.UPDATE.value
        if a.lower()=='delete':
            return CommandType.DELETE.value

    @staticmethod
    def get_by_id(a: int):
        for i in CommandType:
            if a == i.value:
                return i


@dataclass
class Log:
    pass

@dataclass
class ShoppingItem:
    name: str
    quantity: str
    shop: str
    id: str
    list_id: str
    done: bool = False

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
    id: str
    name: str

@dataclass
class ListCommand():
    origin: str
    type: CommandType
    item: ShoppingList
    timestamp: datetime



