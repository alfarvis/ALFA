#!/usr/bin/env python
"""
Define max command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy
from .Stat_Container import StatContainer

# TODO: Combine all stat commands


class StatMax(AbstractCommand):
    """
    Calculate max of an array
    """

    def briefDescription(self):
        return "find maximum of a numerical array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

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
        result_objects = []
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            idx = numpy.logical_not(numpy.isnan(array))
        elif numpy.issubdtype(array.dtype, numpy.datetime64):
            idx = numpy.logical_not(numpy.isnat(array))
        else:
            Printer.Print("The array is not supported type so cannot find max")
            return result_object
        if StatContainer.conditional_array is not None and StatContainer.conditional_array.data.size == array.size:
            idx = numpy.logical_and(idx, StatContainer.conditional_array.data)
        max_val = numpy.max(array[idx])
        idx = numpy.argmax(array[idx])
        if StatContainer.row_labels is not None:
            rl = StatContainer.row_labels.data
            max_rl = rl[idx]
            # Result for max index
            result_object = ResultObject(max_rl, [],
                                         DataType.array,
                                         CommandStatus.Success)

            result_object.createName(
                    StatContainer.row_labels.name,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            result_objects.append(result_object)
        # Result for max value
        result_object = ResultObject(max_val, [],
                                     DataType.array,
                                     CommandStatus.Success)
        result_object.createName(
                array_data.keyword_list,
                command_name=self.commandTags()[0],
                set_keyword_list=True)
        result_objects.append(result_object)
        if StatContainer.row_labels is not None:
            Printer.Print("Maximum of", array_data.name, "is", max_val, "corresponding to", max_rl)
        else:
            Printer.Print("Maximum of", array_data.name, "is", max_val)
        return result_objects

    def ArgNotFoundResponse(self, arg_name):
        super().AnalyzeArgNotFoundResponse(arg_name)

    def MultipleArgsFoundResponse(self, arg_name):
        super().AnalyzeMultipleArgsFoundResponse(arg_name)
