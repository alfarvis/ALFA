#!/usr/bin/env python

import unittest
from Alfarvis.alpharvis_versions.alpha_1_1 import add_basic_database
from Alfarvis.history import TypeDatabase
from Alfarvis.basic_definitions import DataType, searchFileFromFolder


class TestAddBasicDatabase(unittest.TestCase):

    def test_add_basic_database(self):
        history = TypeDatabase()
        add_basic_database(history)
        # Verify history has the start files
        result = history.search(DataType.file_name, ["file", "database"])
        self.assertEqual(len(result), 0)
        result = searchFileFromFolder(["file", "database"], history)
        self.assertTrue("file" in result[0].keyword_list)
        print("Res: ", result[0])
        self.assertTrue(result[0].data.data_type == DataType.csv)
        self.assertTrue(result[0].data.loaded == False)


if __name__ == '__main__':
    unittest.main()
