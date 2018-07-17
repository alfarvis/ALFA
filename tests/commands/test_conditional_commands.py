#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import CommandStatus, DataObject
from Alfarvis.commands.conditional_commands import (LessThan, GreaterThan,
                                                    Between, Contains)
import numpy as np
import pandas as pd
import numpy.testing as npt


class TestConditional(unittest.TestCase):

    def testEvaluateLessThanNumbers(self):
        less_than = LessThan()
        array_data = DataObject(np.arange(10), keyword_list=['array'])
        user_conv = 'Find all array values less than 5'
        user_conv = user_conv.lower()
        target = DataObject(user_conv.split(' '), ['user', 'conversation'])
        arguments = {'array_data': array_data, 'target': target}
        result_object = less_than.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        npt.assert_almost_equal(array_data.data[result_object.data],
                                np.arange(5))
        user_conv = 'Find all array values less than 5 pm'
        user_conv = user_conv.lower()
        arguments['target'] = DataObject(user_conv.split(' '),
                                         ['user', 'conversation'])
        result_object = less_than.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Error)

    def testEvaluateLessThanDates(self):
        less_than = LessThan()
        data = np.array(['13 Jul 1930 - 15:00',
            '13 Jul 1930 - 15:00',
            '14 Jul 1930 - 12:45',
            '14 Jul 1930 - 14:50',
            '15 Jul 1930 - 16:00',
            '16 Jul 1930 - 14:45',
            '17 Jul 1930 - 12:45',
            '17 Jul 1930 - 14:45',
            '18 Jul 1930 - 14:30',
            '19 Jul 1930 - 12:50',
            '19 Jul 1930 - 15:00',
            '20 Jul 1930 - 13:00',
            '20 Jul 1930 - 15:00',
            '21 Jul 1930 - 14:50',
            '22 Jul 1930 - 14:45',
            '26 Jul 1930 - 14:45',
            '27 Jul 1930 - 14:45',
            '30 Jul 1930 - 14:15',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            ''])
        user_conv = 'Find all array values before 1933'
        user_conv = user_conv.lower()
        target = DataObject(user_conv.split(' '), ['user', 'conversation'])
        array_object = DataObject(data, ['date', 'time'])
        arguments = {'array_data': array_object, 'target': target}
        result_object = less_than.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        dates = pd.to_datetime(data)
        npt.assert_almost_equal(dates.year < 1933, result_object.data)
        user_conv = 'Find all array values before 2 pm'
        user_conv = user_conv.lower()
        arguments['target'] = DataObject(user_conv.split(' '), ['user'])
        result_object = less_than.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)

    def testEvaluateBetweenDates(self):
        between = Between()
        data = np.array(['13 Jul 1930 - 15:00',
            '13 Jul 1930 - 15:00',
            '14 Jul 1930 - 12:45',
            '14 Jul 1930 - 14:50',
            '15 Jul 1930 - 16:00',
            '16 Jul 1930 - 14:45',
            '17 Jul 1930 - 12:45',
            '17 Jul 1930 - 14:45',
            '18 Jul 1930 - 14:30',
            '19 Jul 1930 - 12:50',
            '19 Jul 1930 - 15:00',
            '20 Jul 1930 - 13:00',
            '20 Jul 1930 - 15:00',
            '21 Jul 1930 - 14:50',
            '22 Jul 1930 - 14:45',
            '26 Jul 1930 - 14:45',
            '27 Jul 1930 - 14:45',
            '30 Jul 1930 - 14:15',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '27 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            '31 May 1934 - 16:30',
            ''])
        user_conv = 'Find all array values between 2 pm and 6 pm'
        user_conv = user_conv.lower()
        target = DataObject(user_conv.split(' '), ['user', 'conversation'])
        array_object = DataObject(data, ['date', 'time'])
        arguments = {'array_data': array_object, 'target': target}
        result_object = between.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        self.assertEqual(result_object.data[0], True)
        self.assertEqual(result_object.data[2], False)
        self.assertEqual(result_object.data[-1], False)


if __name__ == '__main__':
    unittest.main()
