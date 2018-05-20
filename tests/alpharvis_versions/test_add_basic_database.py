#!/usr/bin/env python

import unittest
from Alfarvis.alpharvis_versions.alpha_1_1 import add_basic_database
from Alfarvis.history import TypeDatabase
from Alfarvis.basic_definitions import DataType


class TestAddBasicDatabase(unittest.TestCase):

    def test_add_basic_database(self):
        history = TypeDatabase()
        add_basic_database(history)
        # Verify history has the start files
        result = history.search(DataType.file_name, ["tumor", "data"])
        self.assertTrue("tumor" in result[0].keyword_list)
        self.assertTrue(result[0].data.data_type==DataType.csv)
        self.assertTrue(result[0].data.loaded==False)
