#!/usr/bin/env python
"""
Keyword search to store indices to data
"""



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
                self.keyword_dict[keyword] = set()
            self.keyword_dict[keyword].add(index)

    def discard(self, keyword_list, index):
        """
        Remove the index from each of
        the keyword specified in list
        """
        for keyword in keyword_list:
            if keyword in self.keyword_dict:
                self.keyword_dict[keyword].discard(index)
                if not self.keyword_dict[keyword]:
                    del self.keyword_dict[keyword]

    def search(self, keyword_list):
        """
        Return the indices which are common
        among all the keywords specified by
        performing an intersection.
        Parameters:
            keyword_list - list of keywords to search for index
        """
        common_index_dict = {}
        max_hit_set = set()
        max_hit_count = 1
        for keyword in keyword_list:
            if keyword not in self.keyword_dict:
                continue
            else:
                current_index_set = self.keyword_dict[keyword]
                intersect = max_hit_set.intersection(current_index_set)
                intersect_empty = (not intersect)
                if not intersect_empty:
                    max_hit_set = intersect
                    max_hit_count = max_hit_count + 1
                for elem in current_index_set:
                    current_hit = 1
                    if elem in common_index_dict:
                        current_hit = common_index_dict[elem] + 1
                    common_index_dict[elem] = current_hit
                    if intersect_empty and (current_hit == max_hit_count):
                        max_hit_set.add(elem)
        return list(max_hit_set)