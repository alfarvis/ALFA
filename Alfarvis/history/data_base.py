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
        self.name_dict = dict()

    def add(self, keyword_list, data_object, add_to_cache=True,
            data_type=None, name=None):
        """
        Add data with specified keyword list to database
        Parameters
            keyword_list - A list of strings to identify data object
        """
        i = len(self.data_objects)
        self.keyword_search.add(keyword_list, i)
        if name is not None:
            self.name_dict[name] = i
        data_object = DataObject(data_object, keyword_list, data_type, name)
        self.data_objects.append(data_object)
        if add_to_cache:
            self.cache.append(data_object)
        return data_object

    def getHitCount(self):
        """
        Current number of hits based on the latest search. Should
        be called after search function
        """
        return self.keyword_search.current_hit_count

    def nameSearch(self, name):
        """
        Search for data object with specified data type and var name
        """
        if name in self.name_dict:
            return self.name_dict[name]
        return None

    def search(self, keyword_list):
        """
        Search for data object with specified keyword list

        Parameters:
            keyword_list - A list of strings to identify data object

        Returns:
            A list of data structs. Each struct contains data and the
            keywords the data was added with
        """
        name_search_result = [self.data_objects[self.name_dict[name]]
                              for name in keyword_list
                              if name in self.name_dict]
        if len(name_search_result) == 0:
            split_keyword_list = [keyword.split('.')
                                  for keyword in keyword_list]
            concat_keyword_list = sum(split_keyword_list, [])
            new_keyword_list = list(filter(None, concat_keyword_list))
            index_list = self.keyword_search.search(new_keyword_list)
            return [self.data_objects[index] for index in index_list]
        else:
            return name_search_result

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
