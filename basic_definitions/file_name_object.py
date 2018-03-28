#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:52:29 2018

This is a class that defines the filename data type
There are two fields that this object contains
 1. Path for the data file
 2. Type of data
"""

from Alfarvis.basic_definitions import DataType

class FileNameObject:
    
    def __init__(self,data_path="",data_type=DataType.number):
        """
        Creates a result object to store in the database
        """
        self.data_type = data_type
        self.path = data_path