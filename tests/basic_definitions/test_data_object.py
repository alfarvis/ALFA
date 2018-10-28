#!/usr/bin/env python3
import unittest
from Alfarvis.basic_definitions import DataObject


class TestDataObject(unittest.TestCase):

    def testCompareDataObjects(self):
        data_object1 = DataObject(1, ['data', '1'])
        data_object2 = DataObject(1, ['data', '2'])
        data_object3 = DataObject(1, ['data', '1'])
        data_object4 = DataObject(1, ['1', 'data'])
        self.assertTrue(data_object1 == data_object3)
        self.assertTrue(data_object1 != data_object2)
        self.assertTrue(data_object1 == data_object4)

if __name__ == '__main__':
    unittest.main()
