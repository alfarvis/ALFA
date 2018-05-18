#!/usr/bin/env python
"""
Keyword search to store indices to data
"""

from .word import Word


class MaxHitKeywordSet(object):
    """
    """

    def __init__(self):
        self.common_index_dict = {}
        self.max_hit_set = set()
        self.max_hit_count = 1


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

    def correctTypo(self, word):
        """
        Check if some combinations of word slices match the dictionary keys
        """
        w = Word(word)
        # TODO Currently double typos are giving random matches like
        # 'the' matches with 'hate' but does not make sense. So will figure
        # that out later.
        return (self.known(w.typos()) or self.known(w.double_typos()))

    def known(self, word_set):
        return (word_set & self.keyword_dict.keys())

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

    def updateMaxHitSet(self, keyword, S):
        """
        update the max hit word set S using elements from keyword.
        Looks at the intersection between index set of keyword and max hit
        set. If intersection is not empty, set max hit set as intersection.
        Also update the hit count of the elements of curren index set and
        add them to max hit set if the hit count reaches the current max.
        """
        current_index_set = self.keyword_dict[keyword]
        intersect = S.max_hit_set.intersection(current_index_set)
        intersect_empty = (not intersect)
        if not intersect_empty:
            S.max_hit_set = intersect
            S.max_hit_count = S.max_hit_count + 1
        for elem in current_index_set:
            current_hit = 1
            if elem in S.common_index_dict:
                current_hit = S.common_index_dict[elem] + 1
            S.common_index_dict[elem] = current_hit
            if intersect_empty and (current_hit == S.max_hit_count):
                S.max_hit_set.add(elem)

    def search(self, keyword_list):
        """
        Return the indices which are common
        among all the keywords specified by
        performing an intersection.
        Parameters:
            keyword_list - list of keywords to search for index
        """

        max_hit_word_set = MaxHitKeywordSet()
        secondary_keyword_set = set()
        for keyword in keyword_list:
            # Try correcting if not in dict
            if keyword not in self.keyword_dict:
                secondary_keyword_set.update(self.correctTypo(keyword))
            else:
                self.updateMaxHitSet(keyword, max_hit_word_set)
        backup_max_hit_set = max_hit_word_set.max_hit_set.copy()
        # Rely on secondary keywords only if we did not find a unique max
        # hit word i.e max hit word set contains multiple words or no words
        N = len(max_hit_word_set.max_hit_set)
        if N is not 1:
            for keyword in secondary_keyword_set:
                self.updateMaxHitSet(keyword, max_hit_word_set)
        # If secondary keywords end up increasing the number of max keywords
        # we disregard the secondary keywords and use the original result
        if N is not 0 and len(max_hit_word_set.max_hit_set) > N:
            max_hit_set = backup_max_hit_set
        else:
            max_hit_set = max_hit_word_set.max_hit_set
        return list(max_hit_set)
