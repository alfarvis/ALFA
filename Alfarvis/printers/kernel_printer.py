#!/usr/bin/env python
from .abstract_printer import AbstractPrinter


class KernelPrinter(AbstractPrinter):
    """
    Simple printer that prints things to kernel
    """

    def Print(self, *args, **kwargs):
        print(*args, **kwargs)
