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

    # This is a datatype that contains a dataframe downloaded from csv
    csv = 2

    # A number represents a constant value. For example if the user wants
    # 5 + 5 then the data type is number otherwise its array
    number = 3

    # A normal numeric array
    array = 4

    string = 5

    # file_name is a meta data type. It contains a path to one of the other
    # data types
    file_name = 6

    #Save in this format once the algorithm has been trained
    trained_model = 7

    # This is the type of algorithm run
    algorithm_arg = 8

    # imdb is image database
    imdb = 9

    # data_base is a meta type which contains files which have databases(i.e
    # other files)
    data_base = 10

    # Logical array which will only have 0s and 1s
    logical_array = 11

    # Provides the current user conversation to command
    user_conversation = 12

    # Provide the history data base to command
    history = 13

    # Figure returned by visualization
    figure = 14

    # User provided string input
    user_string = 15
    
    #alfarvis script (a script file .alpha written in alfarvis)
    alpha_script = 16
    
