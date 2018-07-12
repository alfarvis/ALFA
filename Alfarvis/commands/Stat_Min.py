#!/usr/bin/env python3
"""
Define min command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy


class StatMin(AbstractCommand):
    """
    Calculate min of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify min command
        """
        return ["min", "minimum", "lowest", "smallest"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the min command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate min value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            min_val = numpy.min(array)
            result_object = ResultObject(min_val, [],
                                         DataType.array,
                                         CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            print("Minimum of", array_data.name, "is", min_val)
        else:
            print("The array is not of numeric type so cannot find min")

        return result_object
