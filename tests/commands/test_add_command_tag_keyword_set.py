#!/usr/bin/env python
import unittest
from Alfarvis.commands.Stat_Mean import StatMean
from Alfarvis.basic_definitions import CommandStatus, DataObject
import numpy as np


class TestAddCommandTagKeywordSet(unittest.TestCase):

    def testAddition(self):
        mean_command = StatMean()
        arg = mean_command.argumentTypes()[0]
        data_object = DataObject(np.ones(4), ['random', 'array'])
        arguments = {arg.keyword: data_object}
        result_object = mean_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        self.assertEqual(result_object.keyword_list,
                         set(['mean', 'random', 'array']))
        data_object.keyword_list.append('mean')
        result_object = mean_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        self.assertEqual(result_object.keyword_list,
                         set(['mean', 'random', 'array', 'average']))
        data_object.keyword_list.append('average')
        result_object = mean_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        self.assertEqual(result_object.keyword_list,
                         set(['mean', 'random', 'array', 'average', 'result']))
        data_object.keyword_list.append('result')
        result_object = mean_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        self.assertEqual(result_object.keyword_list,
                         set(['mean', 'random', 'array', 'average', 'result',
                              'secondary']))
        data_object.keyword_list.append('secondary')
        result_object = mean_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        self.assertGreater(result_object.keyword_list,
                           set(['mean', 'random', 'array', 'average', 'result',
                                'secondary']))


if __name__ == '__main__':
    unittest.main()
