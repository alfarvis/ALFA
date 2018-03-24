#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 22:34:24 2018

@author: vishwaparekh
"""

import unittest
from Alfarvis.parsers.parser_class import AlfaDataParser

class TestParserMethods(unittest.TestCase):

    def test_find_intersection(self):
        self.assertEqual(AlfaDataParser.findIntersection([1, 2, 3],[4, 3, 5]), {3})


if __name__ == '__main__':
    unittest.main()

