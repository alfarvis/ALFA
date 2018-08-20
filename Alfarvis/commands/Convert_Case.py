#!/usr/bin/env python
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy as np
import pandas as pd


class ConvertLower(AbstractCommand):
    """
    Convert array to lower case
    """

    def __init__(self, operation='lower'):
        self.operation = operation

    def commandTags(self):
        """
        return tags that are used to identify mean command
        """
        return ["convert", self.operation, self.operation + "case"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the mean command
        """
        return [Argument(keyword="array_data", optional=False,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate average value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data
        N = len(array)

        if N > 0 and isinstance(array[0], str):
            s = pd.Series(array)
            sout = getattr(s.str, self.operation)()
            array_data.data = sout.as_matrix()
            Printer.Print(array_data.data)
            result_object.command_status = CommandStatus.Success
        else:
            Printer.Print("The array is not of string type")
        return result_object


class ConvertCapitalize(ConvertLower):

    def __init__(self):
        super(ConvertCapitalize, self).__init__('capitalize')

    def commandTags(self):
        return ['convert', 'capitalize', 'first character', 'to uppercase']


class ConvertTitle(ConvertLower):

    def __init__(self):
        super(ConvertTitle, self).__init__('title')

    def commandTags(self):
        return ['convert', 'title', 'first character', 'each word', 'to uppercase']
