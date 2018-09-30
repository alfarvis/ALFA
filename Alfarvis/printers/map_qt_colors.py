#!/usr/bin/env python
from PyQt5.QtCore import Qt


def mapColor(color):
    if color == 'r':
        return Qt.red
    elif color == 'b':
        return Qt.blue
    elif color == 'g':
        return Qt.green
    elif color == 'k':
        return Qt.black
    elif color == 'w':
        return Qt.white
    raise RuntimeError("Do not understand color")
