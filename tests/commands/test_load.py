#!/usr/bin/env python3
import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject, FileObject
from Alfarvis import package_directory, create_command_database
from Alfarvis.commands.load import Load
import os


class TestLoad(unittest.TestCase):

    def testSearchingLoad(self):
        command_database = create_command_database()
        result = command_database.search(["load"])
        self.assertEqual(len(result), 1)
        result = command_database.search(["import"])
        self.assertEqual(len(result), 1)

    def testSearchingLoadWithMultipleKeywords(self):
        command_database = create_command_database()
        result = command_database.search(["load", "now"])
        self.assertEqual(len(result), 1)

    def testDataTypes(self):
        load_command = Load()
        argument_types = load_command.argumentTypes()
        self.assertEqual(len(argument_types), 1)
        self.assertFalse(argument_types[0].optional)
        self.assertEqual(argument_types[0].argument_type[0],
                         DataType.file_name)
        self.assertEqual(argument_types[0].tags, [])

    def testEvaluate(self):
        load_command = Load()
        arg = load_command.argumentTypes()[0]
        file_name_data_object = FileObject('', DataType.file_name, '', False)
        file_name_object = DataObject(
            file_name_data_object, ['random', 'file'])
        arguments = {arg.keyword: file_name_object}
        pre_eval_res = load_command.preEvaluate(**arguments)
        arguments['pre_evaluate_results'] = pre_eval_res
        result_object = load_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Error)
        file_name_data_object.path = os.path.join(
            package_directory, 'test_data', 'data.csv')
        file_name_data_object.data_type = DataType.csv
        file_name_object.data = file_name_data_object
        arguments.pop('pre_evaluate_results', None)

        pre_eval_res = load_command.preEvaluate(**arguments)
        arguments['pre_evaluate_results'] = pre_eval_res
        result_objects = load_command.evaluate(**arguments)
        self.assertEqual(
            result_objects[0].command_status, CommandStatus.Success)


if __name__ == '__main__':
    unittest.main()
