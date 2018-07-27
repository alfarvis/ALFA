#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractPrinter(object):
    """
    Base class for printer. Subclasses can be a simple
    kernel printer or GUI printer
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def Print(self, *args, **kwargs):
        pass
