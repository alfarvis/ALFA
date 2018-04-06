#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 18:20:18 2018

@author: vishwaparekh
"""

import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject, FileNameObject
from Alfarvis import package_directory, create_command_database
from Alfarvis.commands.load import Load
from Alfarvis.history import TypeDatabase
from Alfarvis.commands.read_data import ReadData
import os

class TestReadData(unittest.TestCase):
    def setUp(self):
        self.session_history = TypeDatabase()


    def testread_noData(self):
        file_name_data_object = FileNameObject()
        file_name_object = DataObject(file_name_data_object, ['random', 'file'])
        # Test when the file_name object has no info
        result_object = ReadData.read(file_name_object)
        self.assertEqual(result_object[0].command_status, CommandStatus.Error)
        
    def testread_csvData(self):
        file_name_data_object = FileNameObject()
        file_name_object = DataObject(file_name_data_object, ['random', 'file'])
        # Test when the file_name object has a csv
        file_name_data_object.path = os.path.join(package_directory, 'resources/data.csv')
        file_name_data_object.data_type = DataType.csv
        file_name_object.data = file_name_data_object
        result_object = ReadData.read(file_name_object)
        self.assertEqual(result_object[0].command_status, CommandStatus.Success)
        
    def testread_imageData(self):
        file_name_data_object = FileNameObject()
        file_name_object = DataObject(file_name_data_object, ['random', 'file'])
        # Test when the file_name object has a csv
        file_name_data_object.path = os.path.join(package_directory, 'resources/image.jpg')
        file_name_data_object.data_type = DataType.image
        file_name_object.data = file_name_data_object
        result_object = ReadData.read(file_name_object)
        self.assertEqual(result_object[0].command_status, CommandStatus.Success)
        
        
if __name__ == '__main__':
    unittest.main()