#!/usr/bin/env python3
from PyQt5.QtWidgets import QTextEdit
from .map_qt_colors import mapColor


class QCustomTextEdit(QTextEdit):

    def __init__(self, parent=None, max_text_size=32, div=24):
        super(QCustomTextEdit, self).__init__(parent)
        self.div = div
        self.max_text_size = max_text_size
        self.point_size = 16

    def resetFontSize(self):
        cursor = self.textCursor()
        self.selectAll()
        self.setFontPointSize(self.point_size)
        self.setTextCursor(cursor)
        self.setFontPointSize(self.point_size)
        self.setTextBackgroundColor(mapColor('w'))

    def resizeEvent(self, event):
        self.point_size = min(event.size().width() / self.div, self.max_text_size)
        self.resetFontSize()
        QTextEdit.resizeEvent(self, event)
