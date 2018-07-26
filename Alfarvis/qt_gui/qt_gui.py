#!/usr/bin/env python
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QTabWidget
from Alfarvis.windows.qt_window import QtWindow
from Alfarvis.printers.qt_printer import QtPrinter
from Alfarvis.printers.qt_table_printer import QtTablePrinter
from Alfarvis.printers import Printer, TablePrinter
from Alfarvis.windows import Window


class QtGUI(QDialog):
    def __init__(self, parent=None):
        super(QtGUI, self).__init__(parent)
        # Create subcomponents of the GUI
        self.tab_container = QTabWidget()
        self.qt_printer = QtPrinter()
        self.qt_table_printer = QtTablePrinter(self.tab_container)
        self.user_input = QLineEdit()
        # Select global configs
        QtWindow.setParentWidget(self.tab_container)
        Window.selectWindowType(QtWindow)
        Printer.selectPrinter(self.qt_printer)
        TablePrinter.selectPrinter(self.qt_table_printer)
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_container)
        layout.addWidget(self.qt_printer.text_box)
        layout.addWidget(self.user_input)
        self.setLayout(layout)
