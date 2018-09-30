#!/usr/bin/env python
import pandas as pd
#import numpy as np


class HtmlTablePrinter(object):
    """
    Print a table in html format
    """

    def __init__(self):
        self.ncols = 0
        self.nrows = 0
        self.data = []
        self.headers = []
        self.min_column_width = 0

    def setColumnCount(self, ncols):
        if ncols > self.ncols:
            diff = ncols - self.ncols
            self.data = self.data + [['']] * diff
            self.headers = self.headers + [''] * diff
        else:
            self.data = self.data[:ncols]
            self.headers = self.headers[:ncols]
        self.ncols = ncols

    def setRowCount(self, nrows):
        if nrows > self.nrows:
            diff = nrows - self.nrows
            self.data = [d + [''] * diff for d in self.data]
        elif nrows > 0:
            self.data = [d[:nrows] for d in self.data]
        else:
            self.data = [[] for d in self.data]
        self.nrows = nrows

    def rowCount(self):
        return self.nrows

    def insertRow(self, row_index):
        for d in self.data:
            d.append(' ')
        self.nrows = self.nrows + 1

    def setItem(self, row_count, i, qdata):
        self.data[i][row_count] = qdata.text()

    def setHorizontalHeaderLabels(self, headers):
        self.headers = headers

    def horizontalHeader(self):
        pass

    def setMinColumnWidth(self, column_width):
        self.min_column_width = column_width

    def sortItems(self, column_index, order):
        data_dict = {}
        for i, header in enumerate(self.headers):
            data_dict[header] = self.data[i]
        df = pd.DataFrame(data_dict)
        df.sort_values(self.headers[column_index], inplace=True)
        self.data = (df.values.T).tolist()

    def show(self):
        data_dict = {}
        for i, header in enumerate(self.headers):
            data_dict[header] = self.data[i]
        df = pd.DataFrame(data_dict)
        out = df.to_html(col_space=self.min_column_width, index=False)
        out = "<center>\n" + out + "\n </center>"
        return out
