#!/usr/bin/env python
from .abstract_printer import AbstractPrinter
from .map_qt_colors import mapColor
from .map_qt_alignment import mapAlignment, Align
from .qt_custom_text_edit import QCustomTextEdit
from io import StringIO


class QtPrinter(AbstractPrinter):
    """
    Simple printer that prints things to kernel
    """

    def __init__(self):
        self.text_box = QCustomTextEdit()
        self.text_box.setReadOnly(True)
        self.qt_color = mapColor('k')
        self.align = mapAlignment(Align.Left)
        self.text_box.setMinimumWidth(300)
        self.text_box.setFontPointSize(16)
        self.bg_color = mapColor('w')

    def settings(self, color='k', alignment=Align.Left, bgcolor='w'):
        self.qt_color = mapColor(color)
        self.align = mapAlignment(alignment)
        self.bg_color = mapColor(bgcolor)

    def Print(self, *args, **kwargs):
        string_io = StringIO()
        kwargs['file'] = string_io
        kwargs['end'] = ''
        print(*args, **kwargs)
        self.text_box.setTextBackgroundColor(self.bg_color)
        self.text_box.setTextColor(self.qt_color)
        self.text_box.setAlignment(self.align)
        self.text_box.append(string_io.getvalue())
        
        string_io.close()
