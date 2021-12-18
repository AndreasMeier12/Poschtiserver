import unittest
from app.business.merge import merge_lists
from app.business.datatypes import ListCommand, ShoppingList
from datetime import datetime, timedelta
from app.utils import get_uuid_str as uuid

class MyTestCase(unittest.TestCase):

    def test_simple_client(self):
        a = ShoppingList(uuid(), "a")
        command = ListCommand('client', 'create', a, datetime.now())

        res = merge_lists([command])
        self.assertEqual(len(res), 1)

    def test_simple_server(self):
        a = ShoppingList(uuid(), "a")
        command = ListCommand('server', 'create', a, datetime.now())

        res = merge_lists([command])
        self.assertEqual(len(res), 1)

    def test_simple_both(self):
        a = ShoppingList(uuid(), "a")
        b = ShoppingList(uuid(), "b")

        command = ListCommand('server', 'create', a, datetime.now())

        command_b = ListCommand('client', 'create', b, datetime.now() - timedelta(seconds=12))

        res = merge_lists([command, command_b])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[1].name, 'a')
        self.assertEqual(res[0].name, 'b')

    def test_interleaved(self):
        a = ShoppingList(uuid(), "a")
        b = ShoppingList(uuid(), "b")
        c = ShoppingList(uuid(), "c")

        command = ListCommand('server', 'create', a, datetime.now() - timedelta(seconds=12))

        command_b = ListCommand('client', 'create', b, datetime.now() )
        command_c = ListCommand('server', 'create', c, datetime.now() + timedelta(seconds=12))

        res = merge_lists([command, command_b, command_c])
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].name, 'a')
        self.assertEqual(res[1].name, 'b')
        self.assertEqual(res[2].name, 'c')


    def test_interleaved_delete(self):
        a = ShoppingList(uuid(), "a")
        b = ShoppingList(uuid(), "b")
        c = ShoppingList(uuid(), "c")

        command = ListCommand('server', 'create', a, datetime.now() - timedelta(seconds=12))

        command_b = ListCommand('client', 'create', b, datetime.now() )
        command_c = ListCommand('server', 'create', c, datetime.now() + timedelta(seconds=12))
        command_delete = ListCommand('client', 'delete', b, datetime.now() + timedelta(seconds=13))

        res = merge_lists([command, command_b, command_c, command_delete])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].name, 'a')
        self.assertEqual(res[1].name, 'c')



if __name__ == '__main__':
    unittest.main()
