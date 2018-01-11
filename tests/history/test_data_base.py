#!/usr/bin/env python
import unittest
from Alfarvis.history import Database

class TestDatabase(unittest.TestCase):
    def testSearchingObjects(self):
        data_base = Database()
        data_base.add(["dravid", "age"], 20)
        data_base.add(["sachin", "age"], 30)
        data_list = data_base.search(["age"])
        self.assertEqual(len(data_list), 2)
        data_list = data_base.search(["dravid", "age"])
        self.assertEqual(len(data_list), 1)
        self.assertEqual(data_list[0].data, 20)
        self.assertEqual(data_list[0].keyword_list, ["dravid", "age"])

    def testDiscardObjects(self):
        data_base = Database()
        data_base.add(["dravid", "age"], 20)
        data_base.add(["sachin", "age"], 30)
        data_base.add(["kohli", "age"], 30)
        # Only remove dravid age from database
        data_list = data_base.discard(["dravid", "age"])
        data_list = data_base.search(["dravid"])
        self.assertEqual(len(data_list), 0)
        # Sachin's age should not be removed
        data_list = data_base.search(["sachin", "age"])
        self.assertEqual(len(data_list), 1)
        # Remove all age objects
        data_list = data_base.discard(["age"])
        data_list = data_base.search(["sachin", "age"])
        self.assertEqual(len(data_list), 0)
        data_list = data_base.search(["kohli", "age"])
        self.assertEqual(len(data_list), 0)
