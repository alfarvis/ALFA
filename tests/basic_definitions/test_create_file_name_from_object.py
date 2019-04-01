#!/usr/bin/env python3
import unittest
from Alfarvis.basic_definitions import createFileObjectFromName, DataType


class TestCreateFileObjectFromName(unittest.TestCase):
    def testName(self):
        relative_file_name = 'folder/file_adfd_ddfd.png'
        data_object = createFileObjectFromName(relative_file_name)
        self.assertFalse(data_object.data.loaded)
        self.assertEqual(data_object.keyword_list, ['file', 'adfd', 'ddfd'])
        self.assertEqual(data_object.data.data_type, DataType.image)
        absolute_file_name = '/folder/file_adfd_ddfd.xls'
        data_object = createFileObjectFromName(absolute_file_name)
        self.assertEqual(data_object.data.data_type, DataType.csv)

    def testNameWrongExt(self):
        relative_file_name = 'folder/file_adfd_ddfd.ext'
        data_object = createFileObjectFromName(relative_file_name)
        self.assertEqual(data_object, None)


if __name__ == '__main__':
    unittest.main()
