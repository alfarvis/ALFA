#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject
from Alfarvis import command_database, package_directory
from Alfarvis.history import session_history
import os

class TestLoad(unittest.TestCase):
    def testSearchingLoad(self):
        result = command_database.search(["load"])
        self.assertEqual(len(result), 1)
        result = command_database.search(["import"])
        self.assertEqual(len(result), 1)

    def testSearchingLoadWithMultipleKeywords(self):
        result = command_database.search(["load", "now"])
        self.assertEqual(len(result), 1)

    def testDataTypes(self):
        result = command_database.search(["load"])
        load_command = result[0].data
        argument_types = load_command.argumentTypes()
        self.assertEqual(len(argument_types), 1)
        self.assertFalse(argument_types[0].optional)
        self.assertEqual(argument_types[0].argument_type, DataType.file_name)
        self.assertEqual(argument_types[0].tags, [])

    def testEvaluate(self):
        result = command_database.search(["load"])
        load_command = result[0].data
        arg = load_command.argumentTypes()[0]
        file_name_object = DataObject('Random', ['random', 'file'])
        arguments = {arg.keyword:file_name_object}
        self.assertEqual(load_command.evaluate(**arguments), CommandStatus.Error)
        file_name_object.data = os.path.join(package_directory, 'resources/data.csv')
        self.assertEqual(load_command.evaluate(**arguments), CommandStatus.Success)

    def testSavingToHistory(self):
        result = command_database.search(["load"])
        load_command = result[0].data
        arg = load_command.argumentTypes()[0]
        file_name_object = DataObject(os.path.join(package_directory,
                                                   'resources/data.csv'),
                                      ['breast', 'cancer'])
        arguments = {arg.keyword:file_name_object}
        load_command.evaluate(**arguments)
        # Search for csv data from history
        data_object = session_history.search(DataType.csv, ['breast', 'cancer', 'data'])
        self.assertEqual(len(data_object), 1)
        self.assertEqual(data_object[0].keyword_list, ['breast', 'cancer'])
