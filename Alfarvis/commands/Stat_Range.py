#!/usr/bin/env python3
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .Stat_Container import StatContainer
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer, TablePrinter
import numpy
import pandas as pd

class StatRange(AbstractCommand):
    """
    Calculate range of an array
    """

    def briefDescription(self):
        return "find range of a numerical array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

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
        min_val = numpy.min(array[idx])
        range_val = max_val - min_val
        result_object = ResultObject(range_val, [],
                                     DataType.array,
                                     CommandStatus.Success)
        result_object.createName(
                array_data.keyword_list,
                command_name=self.commandTags()[0],
                set_keyword_list=True)
        
        df_new = pd.DataFrame()
        df_new['Feature']=[array_data.name]
        df_new['Range']=[range_val]
        df_new['Minimum']=[min_val]
        df_new['Maximum']=[max_val]
        
        TablePrinter.printDataFrame(df_new)
        #Printer.Print("Range of", array_data.name, "is", range_val,
        #       "from", min_val, "to", max_val)

        return result_object
