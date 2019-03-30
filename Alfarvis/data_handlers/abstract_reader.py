#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractReader(object):
    __metaclass__ = ABCMeta

    @classmethod
    @abstractproperty
    def data_type(self):
        pass

    @abstractproperty
    def read_in_background(self):
        return False

    @abstractmethod
    def preRead(self, file_path, keyword_list):
        raise RuntimeError("Not implemented")

    @abstractmethod
    def read(self, file_path, keyword_list):
        pass
