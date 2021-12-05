import unittest
from app.business import merge
from app.business.datatypes import ShoppingItem, Delete, Update, Create
from datetime import datetime, timedelta


class TestMerging(unittest.TestCase):

    def create_three_item_merge(self):
        item_a = ShoppingItem("a", "", "", 1, 1)
        item_b = ShoppingItem("b", "", "", 1, 1)
        item_c = ShoppingItem("c", "", "", 2, 1)
        command_a = Create(item_a, datetime.now() - timedelta(days=1), "server")
        command_b = Create(item_b, datetime.now() - timedelta(days=0.2), "client")
        command_c = Create(item_c, datetime.now() - timedelta(days=0.1), "server")
        return [command_a, command_c], [command_b]

    def test_simple_create_server(self):
        item = ShoppingItem("a", "", "", 1, 1)
        command = Create(item, datetime.now(), "server")
        res = merge.merge([command], [])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id==1, 1)

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
        server, client = self.create_three_item_merge()
        res = merge.merge(server, client)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].name, "a")
        self.assertEqual(res[1].name, "b")
        self.assertEqual(res[2].name, "c")

    def test_delete(self):
        server, client = self.create_three_item_merge()
        item_a = ShoppingItem("a", "", "", 1, 1)
        delete_command = Delete(item_a, datetime.now(), 'server')
        server.append(delete_command)
        res = merge.merge(client, server)
        self.assertEqual(len(res), 2)


        pass
    def test_update(self):
        server, client = self.create_three_item_merge()
        item_a = ShoppingItem("d", "", "", 1, 1)
        update_command = Update(item_a, datetime.now(), 'server')
        server.append(update_command)
        res = merge.merge(client, server)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].name, "d")

        pass

    def test_update_client(self):
        server, client = self.create_three_item_merge()
        item_a = ShoppingItem("d", "", "", 1, 1)
        update_command = Update(item_a, datetime.now(), 'client')
        client.append(update_command)
        res = merge.merge(client, server)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[1].name, "d")
