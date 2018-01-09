#!/usr/bin/env python
from keyword_search import KeywordSearch
from Alfarvis.basic_definitions import DataObject

class Database(object):
    def __init__(self):
        self.keyword_search = KeywordSearch()
        self.data_objects = []

    def add(self, keyword_list, data_object):
        self.keyword_search.add(keyword_list, len(self.data_objects))
        self.data_objects.append(DataObject(data_object, keyword_list))

    def search(self, keyword_list):
        index_list = self.keyword_search.search(keyword_list)
        return [self.data_objects[index] for index in index_list]

    def discard(self, index):
        self.keyword_search.discard(self.data_objects[index].keyword_list, index)
        del self.data_objects[index]
