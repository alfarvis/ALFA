#!/usr/bin/env python

import unittest
from Alfarvis.alpharvis_versions.alpha_1_1 import add_basic_database
from Alfarvis.history import TypeDatabase
from Alfarvis.basic_definitions import DataType, searchFileFromFolder


class TestAddBasicDatabase(unittest.TestCase):

    def test_add_basic_database(self):
        history = TypeDatabase()
        add_basic_database(history)

if __name__ == '__main__':
    unittest.main()
