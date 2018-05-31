#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 22:21:23 2018

A generic class to store the results generated from command execution
"""
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject


class ResultObject:

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
