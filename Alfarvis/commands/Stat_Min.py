#!/usr/bin/env python3
"""
Define min command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy
from .Stat_Container import StatContainer

class StatMin(AbstractCommand):
    """
    Calculate min of an array
    """

    def briefDescription(self):
        return "find minimum of a numerical array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

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
        result_objects = []
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        array = array_data.data
        if numpy.issubdtype(array.dtype, numpy.number):
            array_filtered = array[numpy.logical_not(numpy.isnan(array))]
        elif numpy.issubdtype(array.dtype, numpy.datetime64):
            array_filtered = array[numpy.logical_not(numpy.isnat(array))]
        else:
            Printer.Print("The array is not supported type so cannot find max")
            return result_object
        min_val = numpy.min(array_filtered)
        idx = numpy.argmin(array_filtered)
        rl = StatContainer.row_labels.data
        min_rl = rl[idx]
        
        #min value
        result_object = ResultObject(min_val, [],
                                     DataType.array,
                                     CommandStatus.Success)
        result_object.createName(
                array_data.keyword_list,
                command_name=self.commandTags()[0],
                set_keyword_list=True)
        result_objects.append(result_object)
        
        #min index
        result_object = ResultObject(min_rl, [],
                                     DataType.array,
                                     CommandStatus.Success)
        
        result_object.createName(
                StatContainer.row_labels.name,
                command_name=self.commandTags()[0],
                set_keyword_list=True)
        result_objects.append(result_object)
        
        Printer.Print("Minimum of", array_data.name, "is", min_val, "corresponding to", min_rl)

        return result_objects
