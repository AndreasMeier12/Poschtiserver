from sqlalchemy.engine import Row


def get_next_list_command_id(a: Row) -> int:
    if len(a) == 1 and a[0] is None:
        return 1
    return a[0] + 1

