#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum


class Align(Enum):
    Left = 1
    Right = 2
    Center = 3


class AbstractTablePrinter(object):
    """
    Base class for table printer. Subclasses can be a simple
    kernel table printer or GUI printer
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self, ncols, col_widths=None, headers=None,
                   alignments=None):
        """
        Initialize the table
        """
        pass

    @abstractmethod
    def addRow(self, *args):
        """
        Add data to table
        """
        pass

    @abstractmethod
    def show(self):
        """
        Shows the table
        """
        pass
