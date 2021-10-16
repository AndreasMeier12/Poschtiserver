import unittest
import merge
from datatypes import ShoppingItem, Command, Delete, Update, Create
from datetime import datetime, timedelta


class TestMerging(unittest.TestCase):
    def test_simple_create_server(self):
        item = ShoppingItem("a", "", "", 1, 1)
        command = Create(item, datetime.now(), "server")
        res = merge.merge([command], [])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id==1, 1)

        print(res)


    def test_create_simple_client(self):
        item = ShoppingItem("a", "", "", 1, 1)
        command = Create(item, datetime.now(), "client")
        res = merge.merge([], [command])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id, 1)

    def test_create_simple_both(self):
        item_a = ShoppingItem("a", "", "", 1, 1)
        item_b = ShoppingItem("b", "", "", 1, 1)
        command_s = Create(item_a, datetime.now() - timedelta(days=1), "server")
        command_c = Create(item_b, datetime.now(), "client")
        res = merge.merge([command_s], [command_c])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].name, "a")
        self.assertEqual(res[1].name, "b")

    def test_create_interleaved(self):
        item_a = ShoppingItem("a", "", "", 1, 1)
        item_b = ShoppingItem("b", "", "", 1, 1)
        item_c = ShoppingItem("c", "", "", 2, 1)
        command_a = Create(item_a, datetime.now() - timedelta(days=1), "server")
        command_b = Create(item_b, datetime.now() - timedelta(days=0.2), "client")
        command_c = Create(item_c, datetime.now() - timedelta(days=0.1), "server")
        res = merge.merge([command_a, command_c], [command_b])
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].name, "a")
        self.assertEqual(res[1].name, "b")
        self.assertEqual(res[2].name, "c")

    def test_delete(self):
        pass
    def test_update(self):
        pass