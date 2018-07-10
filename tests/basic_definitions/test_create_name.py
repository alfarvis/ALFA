#!/usr/bin/env python
import unittest
from Alfarvis.basic_definitions import createName


class TestCreateName(unittest.TestCase):

    def testSimpleName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rms.rms')
        self.assertEqual(components, ['mean', 'rms', 'rms'])

    def testExistingName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {'mean.rms.rms': 'Hello'}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rmsx.rms')
        self.assertEqual(components, ['mean', 'rmsx', 'rms'])
        name_dict[name] = 'Hello'
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rmsx.rmsy')
        self.assertEqual(components, ['mean', 'rmsx', 'rmsy'])

    def testCompositeName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        name_dict[name] = 'Hello'
        command_name = 'median'
        keyword_list1 = components
        keyword_list2 = []
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'median.mean')
        self.assertEqual(components, ['median', 'mean'])

    def testLastResort(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {'mean.rms.rms': 'Hello', 'mean.rmsx.rms': 'Hello',
                     'mean.rmsx.rmsy': 'Hello', 'mean.rmsx.rmsy': 'Hello'}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rmsx.rmsy.1')
        self.assertEqual(components, ['mean', 'rmsx', 'rmsy', '1'])
        name_dict[name] = 'Hello'
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rmsx.rmsy.2')
        self.assertEqual(components, ['mean', 'rmsx', 'rmsy', '2'])
        for i in range(1000):
            name_dict['mean.rmsx.rmsy.' + str(i + 1)] = 'Hello'
        self.assertRaises(RuntimeError, createName, name_dict,
                          keyword_list1, keyword_list2, command_name)


if __name__ == '__main__':
    unittest.main()
