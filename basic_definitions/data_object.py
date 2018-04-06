#!/usr/bin/env python
"""
Defines a data object
"""
import datetime


class DataObject(object):
    """
    Defines a data object that is stored
    in the data base
    """

    def __init__(self, data, keyword_list):
        """
        Constructor. Also stores the time
        when the data is stored.
        Parameters
            data - object to be stored in database
            keyword_list - keywords used to detect
                           object
        """
        self.data = data
        self.keyword_list = keyword_list
        self.time_stamp = datetime.datetime.now()

    def __hash__(self):
        return hash(' '.join(self.keyword_list))

    def __eq__(self, data):
        return ' '.join(self.keyword_list) == ' '.join(data.keyword_list)

    def __ne__(self, data):
        return not self.__eq__(data)
