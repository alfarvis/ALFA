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
    array = 4
    string = 5
    # file_name is a meta data type. It contains a path to one of the other data types
    file_name = 6
    
    trained_model = 7
    algorithm_arg = 8 # This is the type of algorithm run
    #imdb is image database
    imdb = 9


