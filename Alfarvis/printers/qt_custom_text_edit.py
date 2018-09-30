#!/usr/bin/env python3
from PyQt5.QtWidgets import QTextEdit
from .map_qt_colors import mapColor
from PyQt5.QtGui import QImage, QTextCursor, QTextBlockFormat, QTextDocument, QTextImageFormat
from PyQt5.QtCore import QUrl, QVariant, Qt
import os
import datetime


class QCustomTextEdit(QTextEdit):

    def __init__(self, parent=None, max_text_size=32, div=24):
        super(QCustomTextEdit, self).__init__(parent)
        self.div = div
        self.max_text_size = max_text_size
        self.point_size = 16
        self.image_resources = {}
        self.resource_folder = 'notebook_resources_{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())

    def resetFontSize(self):
        cursor = self.textCursor()
        self.selectAll()
        self.setFontPointSize(self.point_size)
        self.setTextCursor(cursor)
        self.setFontPointSize(self.point_size)
        self.setTextBackgroundColor(mapColor('w'))

    def insertImage(self, qimage, image_name):
        self.moveCursor(QTextCursor.End)
        resource_path = os.path.join(self.resource_folder, image_name) + '.png'
        self.document().addResource(QTextDocument.ImageResource, QUrl(resource_path), QVariant(qimage))
        image_format = QTextImageFormat()
        image_format.setName(resource_path)
        cursor = self.textCursor()
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.insertBlock(block_format)
        cursor.insertImage(image_format)
        cursor.insertBlock(block_format)
        self.image_resources[resource_path] = qimage

    def resizeEvent(self, event):
        self.point_size = min(event.size().width() / self.div, self.max_text_size)
        self.resetFontSize()
        QTextEdit.resizeEvent(self, event)
