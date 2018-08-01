#!/usr/bin/env python2
"""
Main executable that calls alpha with specified version
and facilitates communication between user and alpha
through command line

Uses Qt version of things through a GUI
"""
import re
import sys
from Alfarvis import create_alpha_module_dictionary
from Alfarvis.qt_gui import QtGUI
from PyQt5.QtWidgets import QApplication
from Alfarvis.printers import Printer


class UserInputHandler(object):
    def __init__(self, user_input, qt_app, alpha_module_dictionary):
        self.user_input = user_input
        self.qt_app = qt_app
        self.alpha_module_dictionary = alpha_module_dictionary
        self.user_input.returnPressed.connect(self.userPressedEnter)
        self.pattern = re.compile('(L|l)oad (A|a)l(f|ph)a\s*\w*\s*(\d+.?\d*)\w*')
        latest_version = max(alpha_module_dictionary.keys())
        self.alpha = alpha_module_dictionary[latest_version]()

    def userPressedEnter(self):
        input_text = self.user_input.text()
        Printer.UserPrint("User: " + input_text)
        Printer.Print("Alfa: ")
        if input_text == "Bye" or input_text == "bye":
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
                except:
                    Printer.Print("Cannot instantiate alpha")
                    self.alpha = None
            else:
                Printer.Print("No existing version: ", version)
        elif self.alpha is not None:
            out = self.alpha(input_text)
            if out != '':
                Printer.Print(out)
        else:
            Printer.Print("No alpha loaded!")
        self.user_input.clear()


if __name__ == "__main__":  # pragma: no cover
    # Create alpha module dictionary
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    alpha_module_dictionary = create_alpha_module_dictionary()
    qt_gui = QtGUI()
    Printer.Print("Input a text to receive response from Alfarvis")
    Printer.Print("Enter Bye to close the program")
    user_input_handler = UserInputHandler(qt_gui.user_input, app,
                                          alpha_module_dictionary)
    qt_gui.show()
    app.exec_()
