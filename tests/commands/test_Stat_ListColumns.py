#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject
from Alfarvis import package_directory, create_command_database
from Alfarvis.commands.Stat_ListColumns import StatListColumns
import pandas as pd
import os


class TestStatListColumns(unittest.TestCase):

    def testSearchingStatListColumns(self):
        command_database = create_command_database()
        result = command_database.search(["list", "columns"])
        self.assertEqual(len(result), 1)

    def testDataTypes(self):
        list_columns_command = StatListColumns()
        argument_types = list_columns_command.argumentTypes()
        self.assertEqual(len(argument_types), 2)
        self.assertTrue(argument_types[0].optional)
        self.assertEqual(argument_types[0].argument_type, DataType.csv)
        self.assertEqual(argument_types[0].tags, [])
        self.assertFalse(argument_types[1].optional)
        self.assertEqual(argument_types[1].argument_type,
                         DataType.user_conversation)

    def testEvaluate(self):
        list_columns_command = StatListColumns()
        arg = list_columns_command.argumentTypes()[0]
        file_path = os.path.join(
            package_directory, 'resources', 'data.csv')
        data = pd.read_csv(file_path)
        data_object = DataObject(data, ['random', 'dataset'])
        user_conv = DataObject('list categorical columns'.split(' '),
                               ['user', 'conv'])
        arguments = {arg.keyword: data_object, 'user_conv': user_conv}
        result_object = list_columns_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        # Try false data
        data_object.data = [1, 2, 3]
        result_object = list_columns_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Error)


if __name__ == '__main__':
    unittest.main()
