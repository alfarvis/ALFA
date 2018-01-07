#!/usr/bin/env python2

import pandas as pd
from abstract_command import AbstractCommand, CommandStatus
from argument import Argument, ArgumentType
import os


class Load(AbstractCommand):

    def commandTags(self):
        return ["load"]

    def argumentTypes(self):
        return [Argument(keyword="file_name", optional=False, argument_type=ArgumentType.csv)]

    def verifyArguments(self, file_name):
        if type(file_name) != str:
            return False
        return True

    def evaluate(self, file_name):
        command_status = CommandStatus.Error
        if os.path.isfile(args[0]):
            try:
                data = pd.read_csv(args[0])
                command_status = CommandStatus.Success
            except:
                command_status = CommandStatus.Error
        return command_status
