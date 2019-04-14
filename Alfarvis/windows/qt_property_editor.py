#!/usr/bin/env python3
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import (QFormLayout, QLabel, QCheckBox, QLineEdit, QSpinBox,
                             QDoubleSpinBox, QPushButton, QHBoxLayout, QComboBox)
from .map_qt_checkstate import mapBool, mapCheckedState
from .property_editor import PropertyEditor
from PyQt5.QtCore import Qt
import numpy as np


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
            if len(key) > 6 and key[:6] == 'COMBO_':
                continue
            else:
                combo_key = 'COMBO_' + key
                if combo_key in properties:
                    combo_box = QComboBox()
                    combo_box.addItems(properties[combo_key])
                    index = combo_box.findText(value)
                    if index != -1:
                        combo_box.setCurrentIndex(index)
                    combo_box.currentIndexChanged[str].connect(UpdateKey(properties, key))
                    form_layout.addRow(key, combo_box)
                    continue

            if isinstance(value, (bool, np.bool_)):
                check_box = QCheckBox()
                check_box.setCheckState(mapBool(value))
                check_box.stateChanged.connect(UpdateBool(properties, key))
                form_layout.addRow(key, check_box)
            elif isinstance(value, str):
                line_edit = QLineEdit(value)
                line_edit.textChanged.connect(UpdateKey(properties, key))
                form_layout.addRow(key, line_edit)
            elif isinstance(value, (int, np.int_)):
                spin_box = QSpinBox()
                spin_box.setValue(value)
                spin_box.valueChanged.connect(UpdateKey(properties, key))
                form_layout.addRow(key, spin_box)
            elif isinstance(value, float):
                spin_box = QDoubleSpinBox()
                spin_box.setValue(value)
                spin_box.valueChanged.connect(UpdateKey(properties, key))
                form_layout.addRow(key, spin_box)
            else:
                print("Unknown value type", type(value))
        # Connect signals everywhere :)
        update_target = QPushButton()
        update_target.setText("Update")
        close_form = QPushButton()
        close_form.setText("Close")
        close_form.clicked.connect(self.closeForm)
        hlayout = QHBoxLayout()
        hlayout.addWidget(update_target)
        hlayout.addWidget(close_form)
        form_layout.addRow(hlayout)
        return form_layout, update_target

    def updateTarget(self):
        properties = self.result.data[1]
        #print("Updated properties")
        # for key, value in properties.items():
        #    print(key, ": ", value)
        self.result.data[-1](self.result.data)
        # Window show
        self.result.data[0].show()

    def initUI(self):
        if type(self.result.data) != list:
            return
        properties = self.result.data[1]
        form_layout, button = self.fillForm(properties)
        button.clicked.connect(self.updateTarget)
        self.setLayout(form_layout)
        self.show()
