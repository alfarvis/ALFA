#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 22:21:23 2018

A generic class to store the results generated from command execution
"""
from Alfarvis.basic_definitions import DataType, CommandStatus, createName


class ResultObject:
    _name_database = {}

    def __init__(self, data, keyword_list, data_type=DataType.number, command_status=CommandStatus.Success,
                 add_to_cache=False, name=None):
        """
        Creates a result object to store in the database
        """
        self.data_type = data_type
        self.keyword_list = keyword_list
        self.data = data
        self.command_status = command_status
        self.add_to_cache = add_to_cache
        self.name = name

    @classmethod
    def setDatabase(self, name_database):
        self._name_database = name_database

    def removeName(self, name):
        name_set = self._name_database[self.data_type]
        name_set.discard(name)

    def createName(self, keyword_list1, keyword_list2=[], command_name='',
                   set_keyword_list=False):
        """
        Forwards args to create name
        """
        if self.data_type not in self._name_database:
            self._name_database[self.data_type] = set()
        name_set = self._name_database[self.data_type]
        name, components, keyword_flag = createName(name_set, keyword_list1,
                                                    keyword_list2,
                                                    command_name)
        self.name = name
        name_set.add(name)
        if set_keyword_list or keyword_flag:
            self.keyword_list = components
