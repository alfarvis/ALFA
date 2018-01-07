#!/usr/bin/env python
from sets import Set


class KeywordSearch(object):
    """
    Stores keywords and the data index
    in a dictionary. Allows retrieval
    of data index based on keywords
    """

    def __init__(self):
        """
        Create a dictionary for
        keywords
        """
        self.keyword_dict = dict()

    def add(self, keyword_list, index):
        """
        Store the index in each of
        the keyword specified in list
        """
        for keyword in keyword_list:
            if keyword not in self.keyword_dict:
                self.keyword_dict[keyword] = Set()
            self.keyword_dict[keyword].add(index)

    def discard(self, keyword_list, index):
        """
        Remove the index from each of
        the keyword specified in list
        """
        for keyword in keyword_list:
            if keyword in self.keyword_dict:
                self.keyword_dict[keyword].discard(index)

    def search(self, keyword_list):
        """
        Return the indices which are common
        among all the keywords specified by
        performing an intersection.
        Parameters:
            keyword_list - list of keywords to search for index
        """
        common_index_set = []
        for keyword in keyword_list:
            if keyword not in self.keyword_dict:
                continue
            else:
                current_index_set = self.keyword_dict[keyword]
                if not common_index_set:
                    common_index_set = current_index_set
                common_index_set.intersection_update(current_index_set)
        return list(common_index_set)
