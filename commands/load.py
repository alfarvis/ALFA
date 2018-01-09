#!/usr/bin/env python2

import pandas as pd
from abstract_command import AbstractCommand, CommandStatus
from argument import Argument, ArgumentType
import os


class Load(AbstractCommand):

    def commandTags(self):
        return ["load", "import"]

    def argumentTypes(self):
        return [Argument(keyword="file_name", optional=False, argument_type=ArgumentType.string)]

    def evaluate(self, file_name):
        command_status = CommandStatus.Error
        if os.path.isfile(file_name):
            try:
                data = pd.read_csv(file_name)
                command_status = CommandStatus.Success
            except:
                command_status = CommandStatus.Error
        return command_status
