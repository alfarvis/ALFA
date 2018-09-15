#!/usr/bin/env python3
from PyQt5.QtWidgets import QTextEdit
from .map_qt_colors import mapColor

class QCustomTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(QCustomTextEdit, self).__init__(parent)

    def resizeEvent(self, event):
        cursor = self.textCursor()
        point_size = min(event.size().width() / 24.0, 32)
        self.selectAll()
        self.setFontPointSize(point_size)
        self.setTextCursor(cursor)
        self.setFontPointSize(point_size)
        self.setTextBackgroundColor(mapColor('g'))
        QTextEdit.resizeEvent(self, event)
