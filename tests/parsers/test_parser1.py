#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 22:34:24 2018

@author: vishwaparekh
"""

import unittest
from Alfarvis.parsers.parser_class import AlfaDataParser
from Alfarvis.history import TypeDatabase
from Alfarvis.basic_definitions import DataObject, CommandStatus, DataType
from Alfarvis.commands.abstract_command import AbstractCommand
from Alfarvis.commands.argument import Argument


class DummyCommand(AbstractCommand):

    def commandTags(self):
        return ["dummy", "test"]

    def argumentTypes(self):
        return [Argument(keyword="dummy", optional=False, argument_type=DataType.file_name)]

    def evaluate(self, dummy):
        self.history.add(DataType.string, ["dummy", "result"], dummy)
        return CommandStatus.Success


class TestParserMethods(unittest.TestCase):

    def setUp(self):
        self.history = TypeDatabase()
        self.parser = AlfaDataParser(self.history)

    def test_find_intersection(self):
        self.assertEqual(AlfaDataParser.findIntersection(
            [1, 2, 3], [4, 3, 5]), {3})

    def test_print_commands(self):
        command_list = [DataObject(None, ['load']),
                        DataObject(None, ['Random Forrest'])]
        self.parser.printCommands(command_list)

    def test_execute_command(self):
        command = DummyCommand(self.history)
        self.parser.executeCommand(command, {"dummy": "How are you"})
        res = self.history.search(DataType.string, ["dummy"])
        self.assertEqual(len(res), 1)
        data_obj = res[0]
        self.assertEqual(data_obj.data, "How are you")

if __name__ == '__main__':
    unittest.main()
