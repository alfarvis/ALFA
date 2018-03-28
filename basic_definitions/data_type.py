#!/usr/bin/env python
"""
Define data type of data stored in database
"""
from enum import Enum


class DataType(Enum):
    """
    Different types of data stored in database
    """
    image = 1
    csv = 2
    number = 3
    string = 4
    # file_name is a meta data type. It contains a path to one of the other data types
    file_name = 5
    
    trained_model = 6
    algorithm_arg = 7
    #imdb is image database
    imdb = 8


