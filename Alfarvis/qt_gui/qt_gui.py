#!/usr/bin/env python
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QSizePolicy, QCompleter)
from PyQt5.QtCore import QStringListModel
from Alfarvis.qt_gui.qt_custom_line_edit import QCustomLineEdit
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
        self.qt_table_printer = QtTablePrinter()
        self.user_input = QCustomLineEdit()
        self.completion_model = QStringListModel()
        completer = QCompleter()
        completer.setModel(self.completion_model)
        self.user_input.setCompleter(completer)
        # Select global configs
        QtWindow.setParentWidget(self.tab_container)
        Window.selectWindowType(QtWindow)
        Printer.selectPrinter(self.qt_printer)
        TablePrinter.selectPrinter(self.qt_table_printer)
        # Size
        self.qt_printer.text_box.setSizePolicy(QSizePolicy.Minimum,
                                               QSizePolicy.Expanding)
        self.tab_container.setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding)
        self.qt_table_printer.table_widget.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        # Layout
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.qt_printer.text_box, stretch=0)
        h_layout.addWidget(self.tab_container, stretch=2)
        h_layout.addWidget(self.qt_table_printer.table_widget, stretch=1)
        layout.addLayout(h_layout)
        layout.addWidget(self.user_input)
        self.setLayout(layout)
        # Connections
        self.qt_table_printer.table_widget.itemDoubleClicked.connect(self.double_click_table_cell)

    def double_click_table_cell(self, widget_item):
        self.user_input.insert(' ' + widget_item.text() + ' ')
        self.user_input.setFocus()
