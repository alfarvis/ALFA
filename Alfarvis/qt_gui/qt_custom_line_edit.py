#!/usr/bin/env python3
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal


class QCustomLineEdit(QLineEdit):
    upArrowPress = pyqtSignal()
    downArrowPress = pyqtSignal()

    def __init__(self, parent=None):
        super(QCustomLineEdit, self).__init__(parent)

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Up:
            self.upArrowPress.emit()
        elif evt.key() == Qt.Key_Down:
            self.downArrowPress.emit()
        QLineEdit.keyPressEvent(self, evt)
