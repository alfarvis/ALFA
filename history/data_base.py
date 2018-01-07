#!/usr/bin/env python
from keyword_search import KeywordSearch

class Database(object):
    def __init__(self):
        self.keyword_search = KeywordSearch()
        self.data_base = []
        self.data_keyword_lists = []

    def add(self, keyword_list, data_object):
        self.keyword_search.add(keyword_list, len(self.data_base))
        self.data_base.append(data_object)
        self.data_keyword_lists.append(keyword_list)

    def search(self, keyword_list):
        index_list = self.keyword_search.search(keyword_list)
        return [self.data_base[index] for index in index_list]

    def discard(self, index):
        self.keyword_search.discard(self.data_keyword_lists[index], index)
        del self.data_base[index]
        del self.data_keyword_lists[index]
