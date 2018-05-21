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
    # A number represents a constant value. For example if the user wants
    # 5 + 5 then the data type is number otherwise its array
    number = 3
    array = 4
    string = 5
    # file_name is a meta data type. It contains a path to one of the other data types
    file_name = 6
    
    trained_model = 7
    algorithm_arg = 8 # This is the type of algorithm run
    #imdb is image database

    imdb = 9

    # data_base is a meta type which contains files which have databases(i.e other files)
    data_base = 10



