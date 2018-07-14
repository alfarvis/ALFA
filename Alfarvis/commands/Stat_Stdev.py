#!/usr/bin/env python2
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy


class StatStdev(AbstractCommand):
    """
    Calculate stdev of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify stdev command
        """
        return ["stdev", "standard", "deviation"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the stdev command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate stdev value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data
        if numpy.issubdtype(array.dtype, numpy.number):
            array_filtered = array[numpy.logical_not(numpy.isnan(array))]
            std_val = numpy.std(array_filtered)
            result_object = ResultObject(
                std_val, [], DataType.array, CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            print("Standard deviation of", array_data.name, "is", std_val)
        else:
            print("The array is not of numeric type so cannot find stdev")

        return result_object
