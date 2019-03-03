#!/usr/bin/env python

import traceback
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
from Alfarvis.printers import Printer
from Alfarvis.basic_definitions import (CommandStatus,
                                        ResultObject)


class SignalClass(QObject):
    finishedSignal = pyqtSignal('PyQt_PyObject')


class EvaluateCommand(QRunnable):

    def __init__(self, command, arguments, exitFcn):
        super(EvaluateCommand, self).__init__()
        self.command = command
        self.arguments = arguments
        self.signal_class = SignalClass()
        self.signal_class.finishedSignal.connect(exitFcn)

    def run(self):
        try:
            results = self.command.preEvaluate(**self.arguments)
        except Exception as e:
            error = "\n"
            error += "Failed to evaluate {}\n".format(self.command.commandTags()[0])
            error += "save this chat and tag it when creating a bug report\n"
            error += str(traceback.format_exc())
            results = ResultObject(error, None, None, CommandStatus.Error)
        # Signal that you are done with the results of the command
        self.signal_class.finishedSignal.emit(results)
