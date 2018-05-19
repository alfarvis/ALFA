#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:52:29 2018

This is a class that defines the filename data type
There are four fields that this object contains
 1. Path for the data file
 2. Type of data
 3. Description of the file
 4. Whether it is loaded or not
"""

from namedlist import namedlist

FileObject = namedlist(
            'FileObject', field_names='path, data_type, description, loaded')
