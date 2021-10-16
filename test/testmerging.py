import unittest
import merge
from datatypes import ShoppingItem, Command, Delete, Update, Create
from datetime import datetime, timedelta


class TestMerging(unittest.TestCase):
    def test_simple_create_server(self):
        item = ShoppingItem("a", "", "", 1, 1)
        command = Create(item, datetime.now(), "server")
        res = merge.merge([command], [])
        print(res)


    def test_create_simple_client(self):
        item = ShoppingItem("a", "", "", 1, 1)
        command = Create(item, datetime.now(), "client")
        res = merge.merge([], [command])
        print(res)

    def test_create_simple_both(self):
        item_a = ShoppingItem("a", "", "", 1, 1)
        item_b = ShoppingItem("b", "", "", 1, 1)
        command_s = Create(item_a, datetime.now() - timedelta(days=1), "server")
        command_c = Create(item_b, datetime.now(), "client")
        res = merge.merge([command_s], [command_c])
        print(res)

    def test_create_interleaved(self):
        pass
    def test_delete(self):
        pass
    def test_update(self):
        pass