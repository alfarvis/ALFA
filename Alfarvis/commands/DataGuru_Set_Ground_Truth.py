#!/usr/bin/env python3
"""
Set ground truth
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer, TablePrinter
import numpy
import re


class SetGT(AbstractCommand):
    """
    Sets the ground truth for data guru operations
    """

    def commandTags(self):
        """
        return tags that are used to identify set ground truth command
        """
        return ["setgt", "set", "ground", "truth", "labels", "reference"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the set ground truth command
        """
        return [Argument(keyword="array_data", optional=False,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        store ground truth to history
        Parameters:

        """
        if StatContainer.ground_truth is not None:
            TablePrinter.clearBackGround(StatContainer.ground_truth.name)
        StatContainer.ground_truth = array_data
        TablePrinter.highlight(StatContainer.ground_truth.name)
        Printer.Print("Setting ground truth to ", " ".join(
            array_data.keyword_list))
        return ResultObject(None, None, None, CommandStatus.Success)


class ClearGT(AbstractCommand):
    """
    Clear the ground truth
    """

    def commandTags(self):
        """
        return tags that are used to identify clear ground truth command
        """
        return ["cleargt", "clear", "ground", "truth", "labels", "reference"]

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
        if StatContainer.ground_truth is not None:
            TablePrinter.clearBackGround(StatContainer.ground_truth.name)
        StatContainer.ground_truth = None
        Printer.Print("clearing ground truth")
        return ResultObject(None, None, None, CommandStatus.Success)
