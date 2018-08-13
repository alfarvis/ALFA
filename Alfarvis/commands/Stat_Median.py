#!/usr/bin/env python3
"""
Define median command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy


class StatMedian(AbstractCommand):
    """
    Calculate median of an array
    """

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def commandTags(self):
        """
        return tags that are used to identify median command
        """
        return ["median"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the median command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate median value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            array_filtered = array[numpy.logical_not(numpy.isnan(array))]
            median_val = numpy.median(array_filtered)

            result_object = ResultObject(median_val, [],
                                         DataType.array,
                                         CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            Printer.Print("Median of", array_data.name, "is", median_val)
        else:
            Printer.Print("The array is not of numeric type so cannot",
                          "find median")

        return result_object
