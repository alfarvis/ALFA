#!/usr/bin/env python3
"""
Define count (number of values) command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy


class StatCount(AbstractCommand):
    """
    Calculate count
    """

    def commandTags(self):
        """
        return tags that are used to identify count command
        """
        return ["count","number of values"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the count command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate count (number of values) of an array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            array_filtered = array[numpy.logical_not(numpy.isnan(array))]
            count_val = numpy.count_nonzero(array_filtered)

            result_object = ResultObject(count_val, [],
                                         DataType.array,
                                         CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            Printer.Print("Count of", array_data.name, "is", count_val)
        else:
            Printer.Print("The array is not of numeric type so cannot",
                          "find count")

        return result_object
