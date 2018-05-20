#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractReader(object):
    __metaclass__ = ABCMeta

    @classmethod
    @abstractproperty
    def data_type(self):
        pass

    @abstractmethod
    def read(self, file_path, keyword_list):
        pass
