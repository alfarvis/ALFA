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
        self.assertEqual(name, 'mean.x.y')
        self.assertEqual(components, ['mean', 'x', 'y'])

    def testExistingName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y', 'z']
        name_dict = {'mean.x.y': 'Hello'}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.x.y.z')
        self.assertEqual(components, ['mean', 'x', 'y', 'z'])
        name_dict[name] = 'Hello'
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.x.y.z.1')
        self.assertEqual(components, ['mean', 'x', 'y', 'z', '1'])

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
        self.assertEqual(name, 'median.mean.x')
        self.assertEqual(components, ['median', 'mean', 'x'])

    def testLastResort(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x', 'z']
        keyword_list2 = ['rms', 'y', 'a']
        name_dict = {'mean.x.y': 'Hello', 'mean.x.z.y': 'Hello',
                     'mean.x.z.y.a': 'Hello'}
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.x.z.y.a.1')
        self.assertEqual(components, ['mean', 'x', 'z', 'y', 'a', '1'])
        name_dict[name] = 'Hello'
        name, components = createName(name_dict, keyword_list1, keyword_list2,
                                      command_name)
        self.assertEqual(name, 'mean.x.z.y.a.2')
        self.assertEqual(components, ['mean', 'x', 'z', 'y', 'a', '2'])
        for i in range(1000):
            name_dict['mean.x.z.y.a.' + str(i + 1)] = 'Hello'
        self.assertRaises(RuntimeError, createName, name_dict,
                          keyword_list1, keyword_list2, command_name)


if __name__ == '__main__':
    unittest.main()
