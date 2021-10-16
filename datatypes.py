from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC
from datetime import datetime

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



class Command(ABC):
    def get_timestamp(self):
        pass

    def __lt__(self, other):
        return self.get_timestamp() < other.get_timestamp()

    def get_origin(self):
        pass

    def get_id(self):
        pass


class Update(Command):
    def __init__(self, before: ShoppingItem, after: ShoppingItem, timestamp: datetime, origin: str):
        self.before : ShoppingItem = before
        self.after: ShoppingItem = after
        self.timestamp: datetime = timestamp
        self.origin = origin

    def get_before(self) -> ShoppingItem:
        return self.before

    def get_after(self) -> ShoppingItem:
        return self.before

    def get_origin(self):
        return self.origin

    def get_id(self):
        return self.before.id

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
class ShoppingList():
    pass