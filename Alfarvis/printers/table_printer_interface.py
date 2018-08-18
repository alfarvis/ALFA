#!/usr/bin/env python
from .abstract_table_printer import AbstractTablePrinter
from .kernel_table_printer import KernelTablePrinter


class TablePrinter(object):
    selected_table_printer = KernelTablePrinter()

    @classmethod
    def selectPrinter(self, table_printer):
        if not isinstance(table_printer, AbstractTablePrinter):
            raise RuntimeError("table printer not right subclass")
        self.selected_table_printer = table_printer

    @classmethod
    def initialize(self, *args, **kwargs):
        self.selected_table_printer.initialize(*args, **kwargs)

    @classmethod
    def addRow(self, row_name_list, color_fill=None):
        self.selected_table_printer.addRow(row_name_list, color_fill)

    @classmethod
    def show(self):
        self.selected_table_printer.show()

    @classmethod
    def highlight(self, name, color='g'):
        self.selected_table_printer.highlight(name,color)

    @classmethod
    def clearBackGround(self, name):
        self.selected_table_printer.clearBackGround(name)
