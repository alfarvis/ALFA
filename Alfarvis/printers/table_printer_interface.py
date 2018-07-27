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
    def addRow(self, *args):
        self.selected_table_printer.addRow(*args)

    @classmethod
    def show(self):
        self.selected_table_printer.show()
