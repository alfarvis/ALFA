#!/usr/bin/env python
import datetime

class DataObject(object):
    def __init__(self, data, keyword_list):
        self.data = data
        self.keyword_list = keyword_list
        self.time_stamp = datetime.datetime.now()


