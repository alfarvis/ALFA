#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus
from Alfarvis import command_database, package_directory
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
        arguments = {arg.keyword:'Random'}
        self.assertEqual(load_command.evaluate(**arguments), CommandStatus.Error)
        arguments[arg.keyword] = os.path.join(package_directory, 'resources/data.csv')
        self.assertEqual(load_command.evaluate(**arguments), CommandStatus.Success)