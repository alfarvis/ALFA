#!/usr/bin/env python
"""
Database to store data using keywords
"""
from .keyword_search import KeywordSearch
from Alfarvis.basic_definitions import DataObject
from collections import deque


class Database(object):
    """
    Database that allows for storage and retrieval
    of objects using keyword tags
    """

    def __init__(self, cache_len=10):
        """
        Initiate a list to store data and keyword search
        to search for indices
        """
        self.keyword_search = KeywordSearch()
        self.data_objects = []
        self.cache_len = cache_len
        self.cache = deque(maxlen=cache_len)

    def add(self, keyword_list, data_object):
        """
        Add data with specified keyword list to database
        Parameters
            keyword_list - A list of strings to identify data object
        """
        self.keyword_search.add(keyword_list, len(self.data_objects))
        data_object = DataObject(data_object, keyword_list)
        self.data_objects.append(data_object)
        self.cache.append(data_object)

    def search(self, keyword_list):
        """
        Search for data object with specified keyword list

        Parameters:
            keyword_list - A list of strings to identify data object

        Returns:
            A list of data structs. Each struct contains data and the
            keywords the data was added with
        """
        index_list = self.keyword_search.search(keyword_list)
        return [self.data_objects[index] for index in index_list]

    def getLastObject(self, index=0):
        """
        Uses the cache to retrieve an object without search
        Note: Cache is not updated when things are discarded
        Parameters:
            index - Index of the object to retrieve from cache. Index of
                    zero implies latest element in the cache and Index
                    of cache_len - 1 implies the oldest element
        Returns:
            The object corresponding to the index in cache. If cache is
            smaller than index, then returns None
        """
        if index >= len(self.cache):
            return None
        elif index < 0:
            raise RuntimeError("The index should be greater than equal 0")

        return self.cache[-1 - index]

    def discard(self, keyword_list):
        """
        Remove all objects that match the keyword list. Use carefully.

        Parameters
            keyword_list - A list of strings to identify data objects
                           to be removed
        """
        index_list = self.keyword_search.search(keyword_list)
        for index in index_list:
            self.keyword_search.discard(
                self.data_objects[index].keyword_list, index)
            self.data_objects[index] = None
