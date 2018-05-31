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

    def evaluate(self, array_data=None):
        """
        Calculate stdev value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        keyword_set = set(array_data.keyword_list)
        self.addCommandToKeywords(keyword_set)
        array = array_data.data
        if numpy.issubdtype(array.dtype, numpy.number):
            std_val = numpy.std(array)
            print("Standard deviation of ", " ".join(
                keyword_set), " is ", std_val)
            result_object = ResultObject(
                std_val, keyword_set, DataType.array, CommandStatus.Success)
        else:
            print("The array is not of numeric type so cannot find stdev")

        return result_object
