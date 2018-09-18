#!/usr/bin/env python
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QSizePolicy, QCompleter,
                             QSplitter, QLabel, QLineEdit)
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QApplication
from Alfarvis.qt_gui.qt_custom_line_edit import QCustomLineEdit
from Alfarvis.windows.qt_window import QtWindow
from Alfarvis.printers.qt_printer import QtPrinter
from Alfarvis.printers.qt_table_printer import QtTablePrinter
from Alfarvis.printers import Printer, TablePrinter
from Alfarvis.windows import Window
from Alfarvis.commands.Stat_Container import StatContainer


class QtGUI(QDialog):
    label_font = 12
    user_input_font = 18

    def __init__(self, parent=None):
        super(QtGUI, self).__init__(parent)
        # Create subcomponents of the GUI
        self.tab_container = QTabWidget()
        self.qt_printer = QtPrinter()
        self.qt_table_printer = QtTablePrinter()
        self.user_input = QCustomLineEdit()
        self.completion_model = QStringListModel()
        self.labels = [QLineEdit("None"), QLineEdit("None"), QLineEdit("None")]
        self.ground_truth = QLabel()
        self.row_label = QLabel()
        self.filter_label = QLabel()
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
        # Add ref labels
        self.ref_labels = []
        for ref_label in ['Reference', 'Row Label', 'Filter']:
            self.ref_labels.append(QLabel('<span style=" font-size: ' + str(self.label_font) + 'pt; font-weight:600;">' + ref_label + ': </span>'))
            self.ref_labels[-1].setMinimumHeight(0.02 * screen_resolution.height())
        # Font for user input:
        f = self.user_input.font()
        f.setPointSize(self.user_input_font)  # sets the size to 27
        self.user_input.setFont(f)
        f.setPointSize(self.label_font)
        for label in self.labels:
            label.setFont(f)
            label.setMinimumHeight(0.02 * screen_resolution.height())
            label.setReadOnly(True)
        # Size
        self.user_input.setMinimumHeight(0.02 * screen_resolution.height())
        self.qt_printer.text_box.setSizePolicy(QSizePolicy.Minimum,
                                               QSizePolicy.Expanding)
        self.tab_container.setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding)
        self.qt_table_printer.table_widget.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.ground_truth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Layout
        layout = QVBoxLayout()
        # Add gt, rowlabels, filter
        hlayout = QHBoxLayout()
        for i in range(3):
            hlayout.addWidget(self.ref_labels[i])
            hlayout.addWidget(self.labels[i])
        # Add chat,window, tab
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.qt_printer.text_box)
        splitter.addWidget(self.tab_container)
        splitter.addWidget(self.qt_table_printer.table_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 0)
        splitter.setSizes([1, 1000, 500])
        # Final
        layout.addLayout(hlayout)
        layout.addWidget(splitter)
        layout.addWidget(self.user_input)
        self.setLayout(layout)
        # Connections
        self.qt_table_printer.table_widget.itemDoubleClicked.connect(self.double_click_table_cell)

    def updateLabels(self):
        for i, attr_name in enumerate(['ground_truth', 'row_labels', 'conditional_array']):
            data = getattr(StatContainer, attr_name)
            if data is None:
                self.labels[i].setText("None")
            else:
                self.labels[i].setText(data.name)

    def double_click_table_cell(self, widget_item):
        self.user_input.insert(' ' + widget_item.text() + ' ')
        self.user_input.setFocus()
