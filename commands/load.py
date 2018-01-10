#!/usr/bin/env python2
"""
Define load command
"""
import pandas as pd
from Alfarvis.basic_definitions import DataType, CommandStatus
from abstract_command import AbstractCommand
from argument import Argument
import os


class Load(AbstractCommand):
    """
    Loads a csv file
    """

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["load", "import"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for executing
        the load command
        """
        return [Argument(keyword="file_name", optional=False, argument_type=DataType.file_name)]

    def evaluate(self, file_name):
        """
        Load the file name specified and store it in history
        Parameters:
            file_name - Path to the csv file to load
        """
        command_status = CommandStatus.Error
        if os.path.isfile(file_name):
            try:
                data = pd.read_csv(file_name)
                command_status = CommandStatus.Success
            except:
                command_status = CommandStatus.Error
        return command_status
