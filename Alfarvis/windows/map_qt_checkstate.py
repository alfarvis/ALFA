#!/usr/bin/env python3
from PyQt5.QtCore import Qt


def mapBool(state):
    if state:
        return Qt.Checked
    return Qt.Unchecked


def mapCheckedState(state):
    if state == Qt.Checked:
        return True
    return False
