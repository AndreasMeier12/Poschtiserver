from sqlalchemy.engine import Row
from uuid import uuid4

from app.business import datatypes
from app.business.datatypes import ListCommand, ShoppingList, ShoppingItem, Command
from app.models import ListCommandModel, ItemCommandModel


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