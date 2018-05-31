#!/usr/bin/env python
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy


class StatMean(AbstractCommand):
    """
    Compute mean of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify mean command
        """
        return ["mean", "average"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the mean command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate average value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        keyword_set = set(array_data.keyword_list)
        self.addCommandToKeywords(keyword_set)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            mean_val = numpy.mean(array)
            print("Mean of ", " ".join(keyword_set), " is ", mean_val)
            result_object = ResultObject(mean_val, keyword_set,
                                         DataType.array,
                                         CommandStatus.Success)
        else:
            print("The array is not of numeric type so cannot take mean")

        return result_object
