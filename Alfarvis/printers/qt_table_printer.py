#!/usr/bin/env python
from .abstract_table_printer import AbstractTablePrinter, Align
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush


class QtTablePrinter(AbstractTablePrinter):
    """
    Table printer for the kernel
    """

    def __init__(self, tab_container):
        self.table_widget = QTableWidget()
        self.tab_count = tab_container.count()
        self.tab_container = tab_container
        tab_container.addTab(self.table_widget, "Table Data")

    def mapColor(self, color):
        if color == 'r':
            return Qt.red
        elif color == 'b':
            return Qt.blue
        elif color == 'g':
            return Qt.green
        elif color == 'k':
            return Qt.black
        elif color == 'w':
            return Qt.white
        raise RuntimeError("Do not understoond color")

    def mapAlignment(self, alignment):
        if alignment == Align.Left:
            return Qt.AlignLeft
        elif alignment == Align.Right:
            return Qt.AlignRight
        elif alignment == Align.Center:
            return Qt.AlignCenter
        raise RuntimeError("Do not understoond align")

    def initialize(self, ncols, col_widths=None, headers=None,
                   alignments=None):
        """
        Initialize the table
        """
        self.table_widget.setColumnCount(ncols)
        self.table_widget.setRowCount(0)
        table_header = self.table_widget.horizontalHeader()
        for i in range(ncols - 1):
            table_header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        table_header.setSectionResizeMode(ncols - 1, QHeaderView.Stretch)
        if headers is None:
            headers = [''] * ncols
        if alignments is None:
            alignments = [Align.Left] * ncols
        self.table_widget.setHorizontalHeaderLabels(headers)
        for i, alignment in enumerate(alignments):
            h_item = self.table_widget.horizontalHeaderItem(i)
            qt_align = self.mapAlignment(alignment)
            h_item.setTextAlignment(qt_align)

    def addRow(self, row_names, color_fill=None):
        """
        Add data to table
        """
        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)
        if color_fill is not None:
            qt_color = self.mapColor(color_fill)
        else:
            qt_color = None
        for i, data in enumerate(row_names):
            qdata = QTableWidgetItem(data)
            qdata.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if qt_color is not None:
                qdata.setBackground(QBrush(qt_color))
            self.table_widget.setItem(current_row_count, i, qdata)

    def show(self):
        """
        No need since we print it as soon as we add a row
        """
        self.table_widget.show()
        self.tab_container.setCurrentIndex(self.tab_count)

    def highlight(self, name, color='g'):
        qt_color = self.mapColor(color)
        for i in range(self.table_widget.rowCount()):
            if self.table_widget.item(i, 0).text() == name:
                for j in range(self.table_widget.columnCount()):
                    self.table_widget.item(i, j).setBackground(
                            QBrush(qt_color))

    def clearBackGround(self, name):
        qt_color = self.mapColor('w')
        for i in range(self.table_widget.rowCount()):
            if self.table_widget.item(i, 0).text() == name:
                for j in range(self.table_widget.columnCount()):
                    self.table_widget.item(i, j).setBackground(
                            QBrush(qt_color))
