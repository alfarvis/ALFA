#!/usr/bin/env python
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractTablePrinter(object):
    """
    Base class for table printer. Subclasses can be a simple
    kernel table printer or GUI printer
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self, ncols, col_widths=None, headers=None,
                   alignments=None, tabbed=True):
        """
        Initialize the table
        """
        pass

    @abstractmethod
    def addRow(self, row_names, color_fill=None):
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

    def printDataFrame(self, df, col_widths=None, alignments=None):
        """
        Print data frame
        """
        ncols = len(df.columns)
        self.initialize(ncols, col_widths, df.columns, alignments)
        for index, row in df.iterrows():
            row_names = []
            for val in row:
                if type(val) is float:
                    row_names.append('{:.2f}'.format(val))
                else:
                    row_names.append(str(val))
            self.addRow(row_names)

    def sort(self, column_index, ascending):
        return

    def highlight(self, name, color='g'):
        return

    def clearBackGround(self, name):
        return
