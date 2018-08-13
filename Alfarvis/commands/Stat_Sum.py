#!/usr/bin/env python
"""
Define sum command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy


class StatSum(AbstractCommand):
    """
    Compute sum of elements of an array
    """

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def commandTags(self):
        """
        return tags that are used to identify sum command
        """
        return ["sum", "add elements"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the sum command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate sum of all elements of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            array_filtered = array[numpy.logical_not(numpy.isnan(array))]
            mean_val = numpy.mean(array_filtered)
            result_object = ResultObject(mean_val, [],
                                         DataType.array,
                                         CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            Printer.Print("Sum of", array_data.name, "is", mean_val)
        else:
            Printer.Print("The array is not of numeric type so cannot",
                          "take sum")

        return result_object
