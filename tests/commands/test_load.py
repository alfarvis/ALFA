#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject
from Alfarvis import package_directory, create_command_database
from Alfarvis.commands.load import Load
from Alfarvis.history import TypeDatabase
import os

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.session_history = TypeDatabase()

    def testSearchingLoad(self):
        command_database = create_command_database(self.session_history)
        result = command_database.search(["load"])
        self.assertEqual(len(result), 1)
        result = command_database.search(["import"])
        self.assertEqual(len(result), 1)

    def testSearchingLoadWithMultipleKeywords(self):
        command_database = create_command_database(self.session_history)
        result = command_database.search(["load", "now"])
        self.assertEqual(len(result), 1)

    def testDataTypes(self):
        load_command = Load(self.session_history)
        argument_types = load_command.argumentTypes()
        self.assertEqual(len(argument_types), 1)
        self.assertFalse(argument_types[0].optional)
        self.assertEqual(argument_types[0].argument_type, DataType.file_name)
        self.assertEqual(argument_types[0].tags, [])

    def testEvaluate(self):
        load_command = Load(self.session_history)
        arg = load_command.argumentTypes()[0]
        file_name_object = DataObject('Random', ['random', 'file'])
        arguments = {arg.keyword:file_name_object}
        self.assertEqual(load_command.evaluate(**arguments), CommandStatus.Error)
        file_name_object.data = os.path.join(package_directory, 'resources/data.csv')
        self.assertEqual(load_command.evaluate(**arguments), CommandStatus.Success)

    def testSavingToHistory(self):
        load_command = Load(self.session_history)
        arg = load_command.argumentTypes()[0]
        file_name_object = DataObject(os.path.join(package_directory,
                                                   'resources/data.csv'),
                                      ['breast', 'cancer'])
        arguments = {arg.keyword:file_name_object}
        load_command.evaluate(**arguments)
        # Search for csv data from history
        data_object = self.session_history.search(DataType.csv,
                                                  ['breast', 'cancer', 'data'])
        self.assertEqual(len(data_object), 1)
        self.assertEqual(data_object[0].keyword_list, ['breast', 'cancer'])
