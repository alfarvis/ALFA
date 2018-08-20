#!/usr/bin/env python
"""
data base with data type and keyword resolution capabilities
"""

from .data_base import Database
from Alfarvis.basic_definitions import DataType


class TypeDatabase(object):
    """
    Database for storing values based on data type and keywords
    """
    _argument_database = dict()
    last_data_type = None
    last_data_object = None

    def __init__(self, cache_len=10):
        """
        Initiate keyword data base for each data type
        """
        for data_type in DataType:
            if (data_type is not DataType.user_conversation and
                    data_type is not DataType.history):
                self._argument_database[data_type] = Database(cache_len)

    def add(self, data_type, keyword_list, data_object, add_to_cache=True, name=None):
        """
        Add an object with specified keyword list and data type to database
        Parameters:
            data_type - One of the enum types specified in
                        basic_definitions.DataType
            keyword_list - A list of strings used to identify the data object
            data_object - Data to be stored in the database
        """
        self.last_data_type = data_type
        self.last_data_object = self._argument_database[data_type].add(
            keyword_list, data_object, add_to_cache, data_type, name)

    def getHitCount(self, data_type):
        """
        Current number of hits for data type based on the latest search. Should
        be called after search function
        """
        return self._argument_database[data_type].getHitCount()

    def nameSearch(self, data_type, name):
        """
        Search for data object with specified data type and var name
        """
        return self._argument_database[data_type].nameSearch(name)

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

    def getLastObject(self, data_type=None, index=0):
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
        if data_type is None:
            if self.last_data_type is None:
                raise RuntimeError(
                    "Cannot ask for last data type since nothing is present in history yet")
            else:
                return self.last_data_object
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
