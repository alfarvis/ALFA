#!/usr/bin/env python
"""
Database to store data using keywords
"""
from keyword_search import KeywordSearch
from Alfarvis.basic_definitions import DataObject

class Database(object):
    """
    Database that allows for storage and retrieval
    of objects using keyword tags
    """
    def __init__(self):
        """
        Initiate a list to store data and keyword search
        to search for indices
        """
        self.keyword_search = KeywordSearch()
        self.data_objects = []

    def add(self, keyword_list, data_object):
        """
        Add data with specified keyword list to database
        Parameters
            keyword_list - A list of strings to identify data object
        """
        self.keyword_search.add(keyword_list, len(self.data_objects))
        self.data_objects.append(DataObject(data_object, keyword_list))

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

    def discard(self, keyword_list):
        """
        Remove all objects that match the keyword list. Use carefully.

        Parameters
            keyword_list - A list of strings to identify data objects
                           to be removed
        """
        index_list = self.keyword_search.search(keyword_list)
        for index in index_list:
            self.keyword_search.discard(self.data_objects[index].keyword_list, index)
            del self.data_objects[index]
