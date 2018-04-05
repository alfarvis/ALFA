#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 22:21:23 2018

A generic class to store the results generated from command execution
"""
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject

class ResultObject:
    
    def __init__(self,data_object,keyword_list,data_type=DataType.number,command_status=CommandStatus.Success):
        """
        Creates a result object to store in the database
        """
        self.data_type = data_type
        self.keyword_list = keyword_list
        self.data_object = data_object
        self.command_status = command_status
