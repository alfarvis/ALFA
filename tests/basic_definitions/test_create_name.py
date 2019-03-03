#!/usr/bin/env python3
import unittest
from Alfarvis.basic_definitions import createName


class TestCreateName(unittest.TestCase):

    def testSimpleName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {}
        name, components, flag = createName(name_dict, keyword_list1,
                                            keyword_list2, command_name)
        self.assertEqual(name, 'mean.rms.x.rms.y')
        self.assertEqual(components, ['mean', 'rms', 'x', 'rms', 'y'])
        self.assertFalse(flag)

    def testExistingName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y', 'z']
        name_dict = {'mean.rms.x.rms.y.z': 'Hello'}
        name, components, flag = createName(name_dict, keyword_list1,
                                            keyword_list2, command_name)
        self.assertEqual(name, 'mean.rms.x.rms.y.z.1')
        self.assertEqual(components, ['mean', 'rms', 'x', 'rms', 'y', 'z', '1'])
        self.assertTrue(flag)

    def testCompositeName(self):
        command_name = 'mean'
        keyword_list1 = ['rms', 'x']
        keyword_list2 = ['rms', 'y']
        name_dict = {}
        name, components, flag = createName(name_dict, keyword_list1,
                                            keyword_list2, command_name)
        name_dict[name] = 'Hello'
        command_name = 'median'
        keyword_list1 = components
        keyword_list2 = []
        name, components, flag = createName(name_dict, keyword_list1,
                                            keyword_list2, command_name)
        self.assertEqual(name, 'median.mean.rms.x.rms.y')
        self.assertEqual(components, ['median', 'mean', 'rms', 'x', 'rms', 'y'])
        self.assertFalse(flag)

    def testLastResort(self):
        command_name = 'mean'
        keyword_list1 = ['x', 'z']
        keyword_list2 = ['y', 'a']
        name_dict = {'mean.x.y': 'Hello', 'mean.x.z.y': 'Hello',
                     'mean.x.z.y.a': 'Hello'}
        name, components, flag = createName(name_dict, keyword_list1,
                                            keyword_list2, command_name)
        self.assertEqual(name, 'mean.x.z.y.a.1')
        self.assertEqual(components, ['mean', 'x', 'z', 'y', 'a', '1'])
        self.assertTrue(flag)
        name_dict[name] = 'Hello'
        name, components, flag = createName(name_dict, keyword_list1,
                                            keyword_list2, command_name)
        self.assertEqual(name, 'mean.x.z.y.a.2')
        self.assertEqual(components, ['mean', 'x', 'z', 'y', 'a', '2'])
        self.assertTrue(flag)
        for i in range(1000):
            name_dict['mean.x.z.y.a.' + str(i + 1)] = 'Hello'
        self.assertRaises(RuntimeError, createName, name_dict,
                          keyword_list1, keyword_list2, command_name)


if __name__ == '__main__':
    unittest.main()
