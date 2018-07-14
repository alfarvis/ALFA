#!/usr/bin/env python
"""
Define max command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy


class StatMax(AbstractCommand):
    """
    Calculate max of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify max command
        """
        return ["max", "maximum", "highest"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the max command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate max value of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            array_filtered = array[numpy.logical_not(numpy.isnan(array))]
            max_val = numpy.max(array_filtered)
            result_object = ResultObject(max_val, [],
                                         DataType.array,
                                         CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            print("Maximum of", array_data.name, "is", max_val)
        else:
            print("The array is not of numeric type so cannot find max")

        return result_object
