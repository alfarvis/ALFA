#!/usr/bin/env python3
"""
Main executable that calls alpha with specified version
and facilitates communication between user and alpha
through command line

Uses Qt version of things through a GUI
"""
import re
import sys
from Alfarvis import create_alpha_module_dictionary
from Alfarvis.qt_gui import QtGUI, QtNotebookGUI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from Alfarvis.printers import Printer
from collections import deque
from Alfarvis.parsers.parser_states import ParserStates
from Alfarvis.basic_definitions import ThreadPoolManager


class UserInputHandler(object):

    def __init__(self, user_input, completion_model,
                 update_labels, variable_history, qt_app,
                 alpha_module_dictionary):
        self.user_input = user_input
        self.cmp = completion_model
        self.previous_input_text = deque(maxlen=10)
        self.previous_variables = deque(maxlen=5)
        self.buffer_index = -1
        self.update_labels = update_labels
        self.variable_history = variable_history
        self.qt_app = qt_app
        self.alpha_module_dictionary = alpha_module_dictionary
        self.user_input.returnPressed.connect(self.userPressedEnter)
        self.user_input.upArrowPress.connect(self.userPressedUpArrow)
        self.user_input.downArrowPress.connect(self.userPressedDownArrow)
        self.pattern = re.compile(
            '(L|l)oad (A|a)l(f|ph)a\s*\w*\s*(\d+.?\d*)\w*')
        self.timer = QTimer()
        self.timer.timeout.connect(update_labels)
        self.timer.start(1000)  # 1 second
        latest_version = max(alpha_module_dictionary.keys())
        self.alpha = self.alpha_module_dictionary[latest_version]()
        self.initializeAlpha()

    def lastNamesAvailable(self, alpha):
        if (hasattr(alpha, 'parser') and
                hasattr(alpha.parser, 'lastResultNames')):
            return True
        return False

    def initializeAlpha(self):
        self.last_names_available = self.lastNamesAvailable(self.alpha)
        try:
            if self.cmp is not None:
                self.clearModel(self.cmp)
                for key, database in self.alpha.parser.history._argument_database.items():
                    names = database.name_dict.keys()
                    self.addStringListToModel(self.cmp, names)
                cnames = self.alpha.parser.command_database.name_dict.keys()
                self.addStringListToModel(self.cmp, cnames)
        except:
            print("Cannot find names to autocomplete")

    def updateVariables(self):
        if self.alpha.parser.history.last_data_object and (self.alpha.parser.history.last_data_object.name not in self.previous_variables):
            self.previous_variables.appendleft(
                    self.alpha.parser.history.last_data_object.name)
        self.variable_history.initialize(1, headers=['Past Variables'], tabbed=False)
        for past_variable in self.previous_variables:
            self.variable_history.addRow([past_variable])

    def userPressedEnter(self):
        input_text = self.user_input.text()
        Printer.Print("______________________________________________________\n")
        Printer.UserPrint("User: " + input_text)
        Printer.Print("Alfa: ")
        lower_text = input_text.lower()
        lower_text_split = lower_text.split(' ')
        if (('bye' in lower_text_split) or
            (('quit' in lower_text_split or 'exit' in lower_text_split) and
             self.alpha.parser.currentState != ParserStates.command_known_data_unknown)):
            print("Closing threads")
            ThreadPoolManager.close()
            print("Qutting Application!")
            self.qt_app.quit()
            return
        match_out = self.pattern.search(input_text)
        if match_out:
            version = float(match_out.group(4))
            Printer.Print("Trying to load alpha v", version)
            if version in self.alpha_module_dictionary:
                try:
                    self.alpha = self.alpha_module_dictionary[version]()
                    Printer.Print("Successfully loaded alpha version", version)
                    self.initializeAlpha()
                except:
                    Printer.Print("Cannot instantiate alpha")
                    self.alpha = None
            else:
                Printer.Print("No existing version: ", version)
        elif self.alpha is not None:
            out = self.alpha(input_text)
            if out != '':
                Printer.Print(out)
            if self.last_names_available and self.cmp is not None:
                last_names = self.alpha.parser.lastResultNames()
                self.addStringListToModel(self.cmp, last_names)
        else:
            Printer.Print("No alpha loaded!")
        # Update ground truth etc
        self.previous_input_text.appendleft(input_text)
        self.user_input.clear()
        self.buffer_index = -1
        self.updateVariables()

    def userPressedUpArrow(self):
        N = len(self.previous_input_text)
        if N == 0:
            return
        self.buffer_index = min(self.buffer_index + 1, N - 1)
        self.user_input.setText(self.previous_input_text[self.buffer_index])

    def userPressedDownArrow(self):
        if self.buffer_index >= 1:
            self.buffer_index = self.buffer_index - 1
            self.user_input.setText(
                self.previous_input_text[self.buffer_index])
        else:
            self.user_input.setText('')

    def clearModel(self, completion_model):
        N = completion_model.rowCount()
        completion_model.removeRows(0, N)

    def addStringListToModel(self, completion_model, string_list):
        N = completion_model.rowCount()
        for i, string in enumerate(string_list):
            completion_model.insertRow(N + i)
            index = completion_model.index(N + i, 0)
            completion_model.setData(index, string)


def main(gui_type='regular'):
    # Create alpha module dictionary
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    ThreadPoolManager.initialize()
    alpha_module_dictionary = create_alpha_module_dictionary()
    if gui_type == 'notebook':
        qt_gui = QtNotebookGUI()
    else:
        qt_gui = QtGUI()
    Printer.Print("Input a text to receive response from Alfarvis")
    Printer.Print("Enter Bye to close the program")
    user_input_handler = UserInputHandler(qt_gui.user_input,
                                          qt_gui.completion_model,
                                          qt_gui.updateLabels,
                                          qt_gui.variable_history, app,
                                          alpha_module_dictionary)
    qt_gui.showMaximized()
    app.exec_()
    ThreadPoolManager.close()


if __name__ == "__main__":  # pragma: no cover
    main('regular')
