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

    def evaluate(self, array_data=None):
        """
        Calculate range value of the array and store it to history
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
            max_val = numpy.max(VarStore.currArray)
            min_val = numpy.min(VarStore.currArray)
            range_val = max_val - min_val
            print("Range of ", " ".join(keyword_list), " is ", range_val,
                  " from ", min_val, " to ", max_val)
            result_object = ResultObject(range_val, keyword_list,
                                         DataType.array,
                                         CommandStatus.Success)
        else:
            print("The array is not of numeric type so cannot find range")

        return result_object
