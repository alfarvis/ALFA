#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 22:39:51 2018

@author: gowtham
"""

import unittest
from Alfarvis.parsers import AlfaDataParser, ParserStates
from Alfarvis.history import TypeDatabase

class TestParser(unittest.TestCase):
    def setUp(self):
        history = TypeDatabase()
        self.parser = AlfaDataParser(history)
    
    def testClearCommandSearchResults(self):
        self.parser.currentState = ParserStates.command_known_data_unknown
        self.parser.keyword_list = ['hello', 'how', 'are', 'you']
        self.parser.clearCommandSearchResults()
        self.assertEqual(self.parser.getCurrentState(),
                         ParserStates.command_unknown)
        self.assertEqual(self.parser.keyword_list, [])
        self.assertEqual(self.parser.command_search_result, [])
        self.assertEqual(self.parser.argumentsFound, {})
        self.assertEqual(self.parser.argument_search_result, {})