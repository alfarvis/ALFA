#!/usr/bin/env python
from .abstract_printer import AbstractPrinter
from .kernel_printer import KernelPrinter


class Printer(object):
    selected_printer = KernelPrinter()

    @classmethod
    def selectPrinter(self, printer):
        if not isinstance(printer, AbstractPrinter):
            raise RuntimeError("printer not subclass")
        self.selected_printer = printer

    @classmethod
    def Print(self, *args, **kwargs):
        self.selected_printer.Print(*args, **kwargs)
