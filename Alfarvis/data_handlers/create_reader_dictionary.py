#!/usr/bin/env python
"""
Create a dictionary of readers based on data_type
"""
from . import abstract_reader
from Alfarvis.basic_definitions.get_subclasses import get_subclasses


def create_reader_dictionary():
    """
    Iterate through sub-classes of reader and
    create a dictionary based on reader data type.
    The alpha module can be recovered from the dictionary
    using the data type handled by reader
    """
    reader_dictionary = {}
    for reader_class in get_subclasses(abstract_reader.AbstractReader):
        if reader_class.data_type() in reader_dictionary:
            print ("Multiple readers available for the same data type: ",
                   reader_class.data_type())
            continue
        else:
            reader_dictionary[reader_class.data_type()] = reader_class()
    return reader_dictionary
