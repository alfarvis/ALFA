#!/usr/bin/env python2
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore
import numpy
import re


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
        if array_data is not None:
            keyword_list = array_data.keyword_list
            VarStore.SetCurrentArray(array_data.data, " ".join(keyword_list))
        else:
            # This will split the sentence into multiple keywords
            # using anything except a-z,0-9 and + as a partition
            pattern = re.compile('[^a-z0-9]+')
            keyword_list = pattern.split(VarStore.currArray_name)
        if numpy.issubdtype(VarStore.currArray.dtype, numpy.number):
            std_val = numpy.std(VarStore.currArray)
            print("Standard deviation of ", " ".join(
                keyword_list), " is ", std_val)
            result_object = ResultObject(
                std_val, keyword_list, DataType.array, CommandStatus.Success)
        else:
            print("The array is not of numeric type so cannot find stdev")

        return result_object
