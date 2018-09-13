#!/usr/bin/env python3
from PyQt5.QtWidgets import QTextEdit


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
        QTextEdit.resizeEvent(self, event)