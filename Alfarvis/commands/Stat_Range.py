#!/usr/bin/env python2
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy


class StatRange(AbstractCommand):
    """
    Calculate range of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify range command
        """
        return ["range"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the range command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate range value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        keyword_set = set(array_data.keyword_list)
        self.addCommandToKeywords(keyword_set)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            max_val = numpy.max(array)
            min_val = numpy.min(array)
            range_val = max_val - min_val
            print("Range of ", " ".join(keyword_set), " is ", range_val,
                  " from ", min_val, " to ", max_val)
            result_object = ResultObject(range_val, keyword_set,
                                         DataType.array,
                                         CommandStatus.Success)
        else:
            print("The array is not of numeric type so cannot find range")

        return result_object
