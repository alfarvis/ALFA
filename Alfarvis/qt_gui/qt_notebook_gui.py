#!/usr/bin/env python
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QSizePolicy, QCompleter,
                             QSplitter, QLabel, QLineEdit)
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QApplication
from Alfarvis.qt_gui.qt_custom_line_edit import QCustomLineEdit
from Alfarvis.tab_manager.qt_tab_manager import QTabManager
from Alfarvis.windows.qt_notebook_window import QtNotebookWindow
from Alfarvis.windows.qt_property_editor import QtPropertyEditor
from Alfarvis.printers.qt_printer import QtPrinter
from Alfarvis.printers.qt_notebook_table_printer import QtNotebookTablePrinter
from Alfarvis.printers.qt_table_printer import QtTablePrinter
from Alfarvis.printers.qt_custom_text_edit import QCustomTextEdit
from Alfarvis.printers import Printer, TablePrinter
from Alfarvis.windows import Window, PropertyEditor
from Alfarvis.commands.Stat_Container import StatContainer


class QtNotebookGUI(QDialog):
    label_font = 12
    user_input_font = 18

    def __init__(self, parent=None):
        super(QtNotebookGUI, self).__init__(parent)
        # Create subcomponents of the GUI
        self.notebook = QCustomTextEdit(max_text_size=24, div=80)
        self.qt_printer = QtPrinter(self.notebook)
        self.qt_table_printer = QtNotebookTablePrinter(self.notebook)
        self.variable_history = QtTablePrinter()
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
        QtNotebookWindow.parent_notebook = self.notebook
        Window.selectWindowType(QtNotebookWindow)
        PropertyEditor.property_editor_class = QtPropertyEditor
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
        self.notebook.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
        self.qt_table_printer.table_widget.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.variable_history.table_widget.setSizePolicy(
                QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.ground_truth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Layout
        layout = QVBoxLayout()
        # Add gt, rowlabels, filter
        hlayout = QHBoxLayout()
        for i in range(3):
            hlayout.addWidget(self.ref_labels[i])
            hlayout.addWidget(self.labels[i])
        # Add tabs for table and past history
        self.right_tab_widget = QTabWidget()
        self.right_tab_widget.addTab(self.qt_table_printer.table_widget, "Data Summary")
        self.right_tab_widget.addTab(self.variable_history.table_widget, "Past variables")
        # Add separate splitter for table and property editor
        h_splitter = QSplitter(Qt.Vertical)
        h_splitter.addWidget(self.right_tab_widget)
        h_splitter.setStretchFactor(0, 2)
        PropertyEditor.parent_widget = h_splitter
        # Add chat,window, tab
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.notebook)
        splitter.addWidget(h_splitter)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 0)
        splitter.setSizes([1000, 500])
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
