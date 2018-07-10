#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 22:21:23 2018

A generic class to store the results generated from command execution
"""
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject
from itertools import zip_longest
import re


class ResultObject:
    name_pattern = re.compile('^[a-zA-Z0-9.]*$')

    def __init__(self, data, keyword_list, data_type=DataType.number, command_status=CommandStatus.Success,
                 add_to_cache=False):
        """
        Creates a result object to store in the database
        """
        self.data_type = data_type
        self.keyword_list = keyword_list
        self.data = data
        self.command_status = command_status
        self.add_to_cache = add_to_cache

    @classmethod
    def checkName(self, name, name_dict):
        if name in name_dict:
            print("Name:", name, "already in dictionary")
            return False
        return True

    @classmethod
    def createName(self, name_dict, command_name, keyword_list1, keyword_list2=[]):
        """
        Create a unique name from given keyword lists
        """
        name_components = []
        if command_name != '':
            name_components.append(command_name)
        for keyword_list in [keyword_list1, keyword_list2]:
            if len(keyword_list) != 0:
                keyword = keyword_list[0]
                if self.name_pattern.match(keyword):
                    name_components.append(keyword)
        name = '.'.join(name_components)
        if self.checkName(name, name_dict):
            return name, name_components
        else:
            # TODO Try adding remaining elements one by one
            # Try maximum 10 times
            zip_object = zip_longest(keyword_list1[1:], keyword_list2[1:],
                                     fill_value='-')
            for keywords in zip_object:
                if self.name_pattern.match(keywords[0]):
                    name_components[1] = name_components[1] + keywords[0]
                if self.name_pattern.match(keywords[1]):
                    name_components[2] = name_components[2] + keywords[1]
                name = '.'.join(name_components)
                if self.checkName(name, name_dict):
                    return name, name_components

        print("Cannont find an unique name!")
        name_components.append(1)
        for i in range(1000):
            name = '.'.join(name_components)
            if self.checkName(name, name_dict):
                return name, name_components
            name_components[3] = i + 2
        raise RuntimeError("Cannot find a unique name")
