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
        self.assertEqual(name, 'mean.rms.x.rms')
        self.assertEqual(components, ['mean', 'rms', 'x', 'rms'])
        name_dict[name] = 'Hello'
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rms.x.rms.y')
        self.assertEqual(components, ['mean', 'rms', 'x', 'rms', 'y'])

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
        self.assertEqual(name, 'median.mean.rms')
        self.assertEqual(components, ['median', 'mean', 'rms'])

    def testLastResort(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {'mean.rms.rms': 'Hello', 'mean.rms.x.rms': 'Hello',
                     'mean.rms.x.rms.y': 'Hello', 'mean.rms.x.rms.y': 'Hello'}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rms.x.rms.y.1')
        self.assertEqual(components, ['mean', 'rms', 'x', 'rms', 'y', '1'])
        name_dict[name] = 'Hello'
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.rms.x.rms.y.2')
        self.assertEqual(components, ['mean', 'rms', 'x', 'rms', 'y', '2'])
        for i in range(1000):
            name_dict['mean.rms.x.rms.y.' + str(i + 1)] = 'Hello'
        self.assertRaises(RuntimeError, createName, name_dict,
                          keyword_list1, keyword_list2, command_name)


if __name__ == '__main__':
    unittest.main()
