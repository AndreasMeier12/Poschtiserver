import unittest
from datetime import datetime, timedelta
from app.utils import get_uuid_str
from app.business import merge
from app.business.datatypes import ShoppingItem, Command, CommandType


class TestMerging(unittest.TestCase):

    def create_three_item_merge(self):
        item_a = ShoppingItem("a", "", "", get_uuid_str(), "1")
        item_b = ShoppingItem("b", "", "", get_uuid_str(), "1")
        item_c = ShoppingItem("c", "", "", get_uuid_str(), "1")
        command_a = Command(item_a, datetime.now() - timedelta(days=1), "server", CommandType.CREATE)
        command_b = Command(item_b, datetime.now() - timedelta(days=0.2), "client", CommandType.CREATE)
        command_c = Command(item_c, datetime.now() - timedelta(days=0.1), "server", CommandType.CREATE)
        return [command_a, command_c], [command_b]

    def test_simple_create_server(self):
        item = ShoppingItem("a", "", "", get_uuid_str(), "1")
        command = Command(item, datetime.now(), "server", CommandType.CREATE)
        res = merge.merge([command], [])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "a")

    def test_create_simple_client(self):
        item = ShoppingItem("a", "", "", get_uuid_str(), "1")
        command = Command(item, datetime.now(), "client", CommandType.CREATE)
        res = merge.merge([], [command])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "a")

    def test_create_simple_both(self):
        item_a = ShoppingItem("a", "", "", get_uuid_str(), 1)
        item_b = ShoppingItem("b", "", "", get_uuid_str(), 1)
        command_s = Command(item_a, datetime.now() - timedelta(days=1), "server", CommandType.CREATE)
        command_c = Command(item_b, datetime.now(), "client", CommandType.CREATE)
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
        id = server[0].item.id
        item_a = ShoppingItem("a", "", "", id, 1)
        delete_command = Command(item_a, datetime.now(), 'server',CommandType.DELETE)
        server.append(delete_command)
        res = merge.merge(client, server)
        self.assertEqual(len(res), 2)


        pass
    def test_update(self):
        server, client = self.create_three_item_merge()
        item_a = ShoppingItem("d", "", "", server[0].item.id, 1)
        update_command = Command(item_a, datetime.now(), 'server', CommandType.UPDATE)
        server.append(update_command)
        res = merge.merge(client, server)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].name, "d")

        pass

    def test_update_client(self):
        server, client = self.create_three_item_merge()
        item_a = ShoppingItem("d", "", "", client[0].item.id, 1)
        update_command = Command(item_a, datetime.now(), 'client', CommandType.UPDATE)
        client.append(update_command)
        res = merge.merge(client, server)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[1].name, "d")
