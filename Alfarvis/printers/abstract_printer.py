#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty
from .align import Align


class AbstractPrinter(object):
    """
    Base class for printer. Subclasses can be a simple
    kernel printer or GUI printer
    """
    __metaclass__ = ABCMeta

    def settings(self, color='k', alignment=Align.Left):
        return

    @abstractmethod
    def Print(self, *args, **kwargs):
        pass
