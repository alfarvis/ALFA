#!/usr/bin/env python
from .abstract_printer import AbstractPrinter
from PyQt5.QtWidgets import QTextEdit
from io import StringIO


class QtPrinter(AbstractPrinter):
    """
    Simple printer that prints things to kernel
    """

    def __init__(self):
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)

    def Print(self, *args, **kwargs):
        string_io = StringIO()
        kwargs['file'] = string_io
        print(*args, **kwargs)
        self.text_box.insertPlainText(string_io.getvalue())
        string_io.close()
