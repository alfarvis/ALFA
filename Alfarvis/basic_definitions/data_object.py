#!/usr/bin/env python
"""
Defines a data object
"""
import datetime

# TODO Use name to compare two data objects makes it so much easier!!


class DataObject(object):
    """
    Defines a data object that is stored
    in the data base
    """

    def __init__(self, data, keyword_list, data_type=None, name=None):
        """
        Constructor. Also stores the time
        when the data is stored.
        Parameters
            data - object to be stored in database
            keyword_list - keywords used to detect
                           object
        """
        self.data = data
        self.name = name
        self.keyword_list = keyword_list
        self.time_stamp = datetime.datetime.now()
        self.length = len(keyword_list)
        self.data_type = data_type

    def __hash__(self):
        return hash(' '.join(self.keyword_list))

    def __eq__(self, data):
        # Old implementation
        # return ' '.join(self.keyword_list) == ' '.join(data.keyword_list)
        # New implementation
        # 1. Check if the two lists have the same size
        # 2. Check if all the elements in list 1 are also present in list 2
        eqRes = True
        if len(self.keyword_list) == len(data.keyword_list):
            self_list_set = set(self.keyword_list)
            for iterator in range(0, len(data.keyword_list)):
                if data.keyword_list[iterator] not in self_list_set:
                    eqRes = False
        else:
            eqRes = False

        return eqRes

    def __ne__(self, data):
        return not self.__eq__(data)
