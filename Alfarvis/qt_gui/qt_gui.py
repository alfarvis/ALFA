#!/usr/bin/env python
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QSizePolicy, QCompleter,
                             QSplitter)
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QApplication
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
        # Get screen resolution:
        app = QApplication.instance()
        screen_resolution = app.desktop().screenGeometry()
        # Font for user input:
        f = self.user_input.font()
        f.setPointSize(27)  # sets the size to 27
        self.user_input.setFont(f)
        # Size
        self.user_input.setMinimumHeight(0.05 * screen_resolution.height())
        self.qt_printer.text_box.setSizePolicy(QSizePolicy.Minimum,
                                               QSizePolicy.Expanding)
        self.tab_container.setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding)
        self.qt_table_printer.table_widget.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        # Layout
        layout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.qt_printer.text_box)
        splitter.addWidget(self.tab_container)
        splitter.addWidget(self.qt_table_printer.table_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 0)
        splitter.setSizes([1, 1000, 500])
        layout.addWidget(splitter)
        layout.addWidget(self.user_input)
        self.setLayout(layout)
        # Connections
        self.qt_table_printer.table_widget.itemDoubleClicked.connect(self.double_click_table_cell)

    def double_click_table_cell(self, widget_item):
        self.user_input.insert(' ' + widget_item.text() + ' ')
        self.user_input.setFocus()
