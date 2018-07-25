#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractWindow(object):
    """
    Base class for window. Subclasses can be a simple
    matplotlib window or widgetted window
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Create a window and a figure inside
        """
        pass

    @abstractmethod
    def show(self, *args, **kwargs):
        """
        Draw matplotlib figure
        """
        pass

    @abstractmethod
    def gcf(self):
        """
        Get figure associated  with window
        """
        pass
