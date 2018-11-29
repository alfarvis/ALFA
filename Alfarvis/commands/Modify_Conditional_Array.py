#!/usr/bin/env python3
"""
Update conditional array in stat container
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer


class SetConditionalArray(AbstractCommand):
    """
    Sets the ground truth for data guru operations
    """

    def briefDescription(self):
        return "set filter as a logical array"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        return tags that are used to identify set ground truth command
        """
        return ["setca", "set", "conditional", "format", "filter"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the set ground truth command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.logical_array)]

    def evaluate(self, array_data):
        """
        Calculate average value of the array and store it to history
        Parameters:

        """
        StatContainer.conditional_array = array_data
        Printer.Print("Setting filter to ", array_data.name)
        return ResultObject(None, None, None, CommandStatus.Success)

    def ArgNotFoundResponse(self, arg_name):
        Printer.Print("Which condition do you want to set?")

    def ArgFoundResponse(self, arg_name):
        Printer.Print("Found variables")

    def MultipleArgsFoundResponse(self, file_name):
        super().MultipleArgsFoundResponse(file_name, 'conditional variables', 1)


class ClearConditionalArray(AbstractCommand):
    """
    Clear the ground truth
    """

    def briefDescription(self):
        return "clear filter"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        return tags that are used to identify set ground truth command
        """
        return ["clearca", "clear", "conditional", "format", "filter"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the set ground truth command
        """
        return []

    def evaluate(self):
        """
        Calculate average value of the array and store it to history
        Parameters:

        """
        StatContainer.conditional_array = None
        Printer.Print("clearing conditional array")
        return ResultObject(None, None, None, CommandStatus.Success)
