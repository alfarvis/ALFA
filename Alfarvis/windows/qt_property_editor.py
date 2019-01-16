#!/usr/bin/env python3
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import (QFormLayout, QLabel, QCheckBox, QLineEdit, QSpinBox,
                             QDoubleSpinBox, QPushButton, QHBoxLayout, QComboBox)
from .map_qt_checkstate import mapBool, mapCheckedState
from .property_editor import PropertyEditor
from PyQt5.QtCore import Qt


class UpdateKey(object):

    def __init__(self, properties, key):
        self.properties = properties
        self.key = key

    def __call__(self, value):
        self.properties[self.key] = value


class UpdateBool(UpdateKey):

    def __init__(self, properties, key):
        super(UpdateBool, self).__init__(properties, key)

    def __call__(self, state):
        self.properties[self.key] = mapCheckedState(state)


class QtPropertyEditor(QWidget):

    def __init__(self, result):
        self.result = result
        super(QtPropertyEditor, self).__init__()
        self.initUI()

    def closeForm(self):
        PropertyEditor.closePreviousPropertyEditor()

    def fillForm(self, properties):
        form_layout = QFormLayout()
        for key, value in properties.items():
            if type(value) == bool:
                check_box = QCheckBox()
                check_box.setCheckState(mapBool(value))
                check_box.stateChanged.connect(UpdateBool(properties, key))
                form_layout.addRow(key, check_box)
            elif type(value) == str:
                line_edit = QLineEdit(value)
                line_edit.textChanged.connect(UpdateKey(properties, key))
                form_layout.addRow(key, line_edit)
            elif type(value) == int:
                spin_box = QSpinBox()
                spin_box.setValue(value)
                spin_box.valueChanged.connect(UpdateKey(properties, key))
                form_layout.addRow(key, spin_box)
            elif type(value) == double:
                spin_box = QDoubleSpinBox()
                spin_box.setValue(value)
                spin_box.valueChanged.connect(UpdateKey(properties, key))
                form_layout.addRow(key, spin_box)

        # Connect signals everywhere :)
        update_figure = QPushButton()
        update_figure.setText("Update")
        close_form = QPushButton()
        close_form.setText("Close")
        close_form.clicked.connect(self.closeForm)
        hlayout = QHBoxLayout()
        hlayout.addWidget(update_figure)
        hlayout.addWidget(close_form)
        form_layout.addRow(hlayout)
        return form_layout, update_figure

    def updateFigure(self):
        properties = self.result.data[1]
        #print("Updated properties")
        # for key, value in properties.items():
        #    print(key, ": ", value)
        self.result.data[-1](self.result.data)

    def initUI(self):
        if type(self.result.data) != list:
            return
        properties = self.result.data[1]
        form_layout, button = self.fillForm(properties)
        button.clicked.connect(self.updateFigure)
        self.setLayout(form_layout)
        self.show()
