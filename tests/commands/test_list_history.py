#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import DataType, DataObject, CommandStatus
from Alfarvis import create_command_database
from Alfarvis.commands.list_history import ListHistory
from Alfarvis.history import TypeDatabase
import numpy as np


class TestListHistory(unittest.TestCase):

    def testSearchingListHistory(self):
        command_database = create_command_database()
        result = command_database.search(["list", "history"])
        self.assertEqual(len(result), 1)

    def testDataTypes(self):
        list_history_command = ListHistory()
        argument_types = list_history_command.argumentTypes()
        self.assertEqual(len(argument_types), 2)
        self.assertFalse(argument_types[0].optional)
        self.assertEqual(argument_types[0].argument_type, DataType.history)
        self.assertEqual(argument_types[0].tags, [])
        self.assertFalse(argument_types[1].optional)
        self.assertEqual(argument_types[1].argument_type,
                         DataType.user_conversation)
        self.assertEqual(argument_types[1].tags, [])

    def testEvaluate(self):
        list_history_command = ListHistory()
        arg1 = list_history_command.argumentTypes()[0]
        arg2 = list_history_command.argumentTypes()[1]
        history = TypeDatabase()
        history.add(DataType.number, ['my', 'lucky', 'number'], 10)
        history.add(DataType.string, [
                    'my', 'favorite', 'quote'], 'Pen is sharper than knife')
        history.add(DataType.array, ['zero', 'array'], np.zeros(10))
        arguments = {arg1.keyword: DataObject(history, 'history'),
                     arg2.keyword: DataObject([], 'user_conv')}
        result_object = list_history_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        # Try no data
        arguments = {arg1.keyword: None, arg2.keyword: DataObject([], '')}
        result_object = list_history_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Error)


if __name__ == '__main__':
    unittest.main()
