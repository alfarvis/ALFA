#!/usr/bin/env python

from data_base import Database
from Alfarvis.basic_definitions import ArgumentType

class ArgumentDatabase:
    _argument_database = dict()
    def __init__(self):
        for argument_type in ArgumentType:
            self._argument_database[argument_type] = Database()
    
    def add(self, argument_type, keyword_list, data_object):
        self._argument_database[argument_type].add(keyword_list, data_object)

    def search(self, argument_type, keyword_list):
        return self._argument_database[argument_type].search(keyword_list)

    def discard(self, argument_type, index):
        self._argument_database[argument_type].discard(index)
