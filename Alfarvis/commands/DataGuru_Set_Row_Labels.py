#!/usr/bin/env python3
"""
Set Row labels
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer, TablePrinter
import numpy
import re


class SetRowLabels(AbstractCommand):
    """
    Sets the row labels for data guru operations
    """

    def commandTags(self):
        """
        return tags that are used to identify set row labels command
        """
        return ["setrl", "set","row","labels"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the set row label command
        """
        return [Argument(keyword="array_data", optional=False,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        set row label
        Parameters:

        """
        if StatContainer.row_labels is not None:
            TablePrinter.clearBackGround(StatContainer.row_labels.name)
        StatContainer.row_labels = array_data
        TablePrinter.highlight(StatContainer.row_labels.name,color='b')
        Printer.Print("Setting row label to ", " ".join(
            array_data.keyword_list))
        return ResultObject(None, None, None, CommandStatus.Success)

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to set as row labels?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to set as row labels?")

class ClearRL(AbstractCommand):
    """
    Clear the row labels
    """

    def commandTags(self):
        """
        return tags that are used to identify set ground truth command
        """
        return ["clearrl", "clear", "row labels"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the clear row labels command
        """
        return []

    def evaluate(self):
        """
        Calculate average value of the array and store it to history
        Parameters:

        """
        if StatContainer.row_labels is not None:
            TablePrinter.clearBackGround(StatContainer.row_labels.name)
        StatContainer.row_labels = None
        Printer.Print("clearing row labels")
        return ResultObject(None, None, None, CommandStatus.Success)
