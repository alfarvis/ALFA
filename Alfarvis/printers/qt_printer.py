#!/usr/bin/env python
from .abstract_printer import AbstractPrinter
from .map_qt_colors import mapColor
from .map_qt_alignment import mapAlignment, Align
from .qt_custom_text_edit import QCustomTextEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtPrintSupport import QPrinter
from io import StringIO
import os


class QtPrinter(AbstractPrinter):
    """
    Simple printer that prints things to kernel
    """

    def __init__(self, text_box=None):
        if text_box is not None:
            self.text_box = text_box
        else:
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

    def save(self, name):
        file_name = QFileDialog.getSaveFileName()
        text = self.text_box.toHtml()
        if file_name:
            name = file_name[0]
            if name[-4:] != 'html':
                name = name + '.html'
            try:
                text_file = open(name, 'w')
                text_file.write(text)
                text_file.close()
                parent_folder = os.path.dirname(name)
            except:
                print("Failed to save text")

            try:
                print(os.path.join(parent_folder, self.text_box.resource_folder))
                os.mkdir(os.path.join(parent_folder, self.text_box.resource_folder))
            except:
                print("Directory cannot be created")

            for resource_name in self.text_box.image_resources:
                resource_path = os.path.join(parent_folder, resource_name)
                print("Saving: ", resource_path)
                self.text_box.image_resources[resource_name].save(resource_path)
            self.Print("Saving notebook to ", name)

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
