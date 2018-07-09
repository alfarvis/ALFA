#!/usr/bin/env python3
import unittest
import numpy as np
from Alfarvis.commands.Stat_Container import StatContainer


class TestStatContainer(unittest.TestCase):

    def testRemoveCommonNames(self):
        input_names = ['abc_def', 'abc_fhg', 'fhgi_abc']
        out_names, common_name = StatContainer.removeCommonNames(input_names)
        self.assertEqual(out_names, ['def', 'fhg', 'fhgi'])
        self.assertEqual(common_name, 'abc')

    def testIsCategorical(self):
        num_categorical_array = np.hstack(([1] * 50, [2] * 50, [5] * 25))
        out = StatContainer.isCategorical(num_categorical_array)
        self.assertEqual(set(out), set([1, 2, 5]))
        str_categorical_array = np.hstack(
            (['Rama'] * 50, ['Krishna'] * 50, ['Bheem'] * 25))
        out = StatContainer.isCategorical(str_categorical_array)
        self.assertEqual(set(out), set(['Rama', 'Krishna', 'Bheem']))
        small_str_categorical = np.array(['Rama', 'Krishna', 'Bheem'] * 2)
        out = StatContainer.isCategorical(small_str_categorical)
        self.assertEqual(set(out), set(['Rama', 'Krishna', 'Bheem']))
        non_categorical_array = np.random.sample(50)
        out = StatContainer.isCategorical(non_categorical_array)
        self.assertEqual(out, None)
        mixed_array = np.array([1, 2, 'object'], dtype=object)
        out = StatContainer.isCategorical(mixed_array)
        self.assertEqual(out, None)
        #mixed_categorical = np.array(['object', 1, 2])

if __name__ == '__main__':
    unittest.main()
