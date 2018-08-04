#!/usr/bin/env python3
from PyQt5.QtWidgets import QLineEdit, QCompleter
from PyQt5.QtCore import Qt, pyqtSignal, QEvent


class QCustomLineEdit(QLineEdit):
    upArrowPress = pyqtSignal()
    downArrowPress = pyqtSignal()

    def __init__(self, parent=None):
        super(QCustomLineEdit, self).__init__(parent)
        self.completer = None
        self.in_auto_completion = False
        self.user_selection = False

    def setCompleter(self, completer):
        if completer:
            try:
                completer.activated.disconnect()
            except:
                pass
            try:
                completer.highlighted.disconnect()
            except:
                pass
            completer.setWidget(self)
            completer.setCompletionMode(QCompleter.PopupCompletion)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.activated.connect(self.insertCompletion)
            completer.highlighted.connect(self.insertCompletion)
            completer.popup().clicked.connect(self.popupClicked)
        self.completer = completer

    def popupClicked(self, model_index):
        print("User pressed enter on popup")
        self.in_auto_completion = False

    def insertCompletion(self, string):
        current_tup = self.text().rsplit(' ', 1)
        in_text = current_tup[0]
        if len(current_tup) == 1:
            in_text = ''
        self.setText(in_text + ' ' + string)
        self.user_selection = True

    def event(self, evt):
        completer = self.completer
        if completer is None:
            return QLineEdit.event(self, evt)
        if evt.type() == QEvent.KeyPress and evt.key() == Qt.Key_Tab:
            self.in_auto_completion = not self.in_auto_completion
            if not self.in_auto_completion:
                if not self.user_selection:
                    self.insertCompletion(completer.currentCompletion())
                self.user_selection = False
                completer.setCompletionPrefix('')
                completer.popup().hide()
            else:
                completion_prefix = self.text().rsplit(' ')[-1]
                completer.setCompletionPrefix(completion_prefix)
                completer.complete()
            return True
        if self.in_auto_completion and evt.type() == QEvent.KeyPress:
            if evt.key() == Qt.Key_Space:
                self.in_auto_completion = False
                self.user_selection = False
                completer.setCompletionPrefix('')
                completer.popup().hide()
            elif evt.key() == Qt.Key_Enter or evt.key() == Qt.Key_Return:
                self.in_auto_completion = False
                if not self.user_selection:
                    self.insertCompletion(completer.currentCompletion())
                self.user_selection = False
                completer.setCompletionPrefix('')
                completer.popup().hide()
                return True
            else:
                completion_prefix = self.text().rsplit(' ')[-1]
                completer.setCompletionPrefix(completion_prefix)
                completer.complete()

        return QLineEdit.event(self, evt)

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Up:
            self.upArrowPress.emit()
        elif evt.key() == Qt.Key_Down:
            self.downArrowPress.emit()
        QLineEdit.keyPressEvent(self, evt)
