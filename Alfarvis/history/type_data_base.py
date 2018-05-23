#!/usr/bin/env python
"""
data base with data type and keyword resolution capabilities
"""

from .data_base import Database
from Alfarvis.basic_definitions import DataType


class TypeDatabase:
    """
    Database for storing values based on data type and keywords
    """
    _argument_database = dict()

    def __init__(self, cache_len=10):
        """
        Initiate keyword data base for each data type
        """
        for data_type in DataType:
            self._argument_database[data_type] = Database(cache_len)

    def add(self, data_type, keyword_list, data_object):
        """
        Add an object with specified keyword list and data type to database
        Parameters:
            data_type - One of the enum types specified in
                        basic_definitions.DataType
            keyword_list - A list of strings used to identify the data object
            data_object - Data to be stored in the database
        """
        self._argument_database[data_type].add(keyword_list, data_object)

    def search(self, data_type, keyword_list):
        """
        Search for data object with specified data type and keyword list

        Parameters:
            data_type - One of the enum types specified in
                        basic_definitions.DataType
            keyword_list - A list of strings to identify data object

        Returns:
            A list of data structs. Each struct contains data and the
            keywords the data was added with
        """
        return self._argument_database[data_type].search(keyword_list)

    def getLastObject(self, data_type, index=0):
        """
        Get the last object of data type from cache
        Parameters:
            data_type - One of the enum types specified in
                        basic_definitions.DataType
            index - Index of the object to retrieve from cache. Index of
                    zero implies latest element in the cache and Index
                    of cache_len - 1 implies the oldest element
        Returns:
            The object corresponding to the index in cache. If cache is
            smaller than index, then returns None
        """
        return self._argument_database[data_type].getLastObject(index)

    def discard(self, data_type, keyword_list):
        """
        Remove data from database. Given a keyword list
        removes the entries corresponding to all data objects
        that are obtained from searching keywords. Use carefully.

        Parameters
            data_type - One of the enum types specified in
                        basic_definitions.DataType
            keyword_list - A list of strings to identify data objects
                        to be removed
        """
        self._argument_database[data_type].discard(keyword_list)
