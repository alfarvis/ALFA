#!/usr/bin/env python
from .abstract_table_printer import AbstractTablePrinter
from .map_qt_alignment import mapAlignment, Align
from .map_qt_colors import mapColor
from .html_table_printer import HtmlTablePrinter
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QTextCursor


class QtNotebookTablePrinter(AbstractTablePrinter):
    """
    Table printer for the kernel
    """

    def __init__(self, text_edit):
        self.table_widget = QTableWidget()  # For non-tabbed case
        self.html_table_widget = None
        self.tab_initialized = False
        self.table_text = ""
        self.text_edit = text_edit

    def initialize(self, ncols, col_widths=None, headers=None,
                   alignments=None, tabbed=True):
        """
        Initialize the table
        """
        if tabbed:
            # Use Html table
            self.html_table_widget = HtmlTablePrinter()
            if col_widths:
                self.html_table_widget.setMinColumnWidth(min(col_widths))
            self.tab_initialized = True
            table_widget = self.html_table_widget
        else:
            table_widget = self.table_widget
            self.tab_initialized = False
        table_widget.setColumnCount(ncols)
        table_widget.setRowCount(0)
        if headers is None:
            headers = [''] * ncols
        table_widget.setHorizontalHeaderLabels(headers)
        table_header = table_widget.horizontalHeader()
        if table_header:
            for i in range(ncols):
                table_header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            if alignments is None:
                alignments = [Align.Left] * ncols
            for i, alignment in enumerate(alignments):
                h_item = table_widget.horizontalHeaderItem(i)
                qt_align = mapAlignment(alignment)
                h_item.setTextAlignment(qt_align)
            table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def addRow(self, row_names, color_fill=None):
        """
        Add data to table
        """
        if self.tab_initialized:
            table_widget = self.html_table_widget
        else:
            table_widget = self.table_widget
        current_row_count = table_widget.rowCount()
        table_widget.insertRow(current_row_count)
        if color_fill is not None:
            qt_color = mapColor(color_fill)
        else:
            qt_color = None
        for i, data in enumerate(row_names):
            qdata = QTableWidgetItem(data)
            qdata.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if qt_color is not None:
                qdata.setBackground(QBrush(qt_color))
            table_widget.setItem(current_row_count, i, qdata)

    def show(self):
        """
        No need since we print it as soon as we add a row
        """
        if self.tab_initialized:
            self.text_edit.moveCursor(QTextCursor.End)
            self.text_edit.setTextColor(mapColor('k'))
            self.text_edit.append('\n')
            self.text_edit.setAlignment(Qt.AlignCenter)
            self.text_edit.append(self.html_table_widget.show())
            self.text_edit.resetFontSize()
        else:
            self.table_widget.show()

    def highlight(self, name, color='g'):
        if not self.tab_initialized:
            table_widget = self.table_widget
            qt_color = mapColor(color)
            for i in range(table_widget.rowCount()):
                if table_widget.item(i, 0).text() == name:
                    for j in range(table_widget.columnCount()):
                        table_widget.item(i, j).setBackground(
                                QBrush(qt_color))

    def sort(self, column_index, ascending):
        if self.tab_initialized:
            table_widget = self.html_table_widget
        else:
            table_widget = self.table_widget
        if ascending:
            table_widget.sortItems(column_index, Qt.AscendingOrder)
        else:
            table_widget.sortItems(column_index, Qt.DescendingOrder)

    def clearBackGround(self, name):
        if not self.tab_initialized:
            table_widget = self.table_widget
            qt_color = mapColor('w')
            for i in range(table_widget.rowCount()):
                if table_widget.item(i, 0).text() == name:
                    for j in range(table_widget.columnCount()):
                        table_widget.item(i, j).setBackground(
                                QBrush(qt_color))
