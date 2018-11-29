#!/usr/bin/env python
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer, TablePrinter
import numpy
import pandas as pd


class StatMean(AbstractCommand):
    """
    Compute mean of an array
    """

    def briefDescription(self):
        return "find mean of a numerical array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

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
        array = array_data.data

        if numpy.issubdtype(array.dtype, numpy.number):
            idx = numpy.logical_not(numpy.isnan(array))
            if StatContainer.conditional_array is not None and StatContainer.conditional_array.data.size == array.size:
                idx = numpy.logical_and(idx, StatContainer.conditional_array.data)
            mean_val = numpy.mean(array[idx])
            result_object = ResultObject(mean_val, [],
                                         DataType.array,
                                         CommandStatus.Success)
            result_object.createName(
                    array_data.keyword_list,
                    command_name=self.commandTags()[0],
                    set_keyword_list=True)
            #Printer.Print("Mean of", array_data.name, "is", mean_val)
            df_new = pd.DataFrame()
            df_new['Feature']=[array_data.name]
            df_new['Mean']=[mean_val]
            TablePrinter.printDataFrame(df_new)
        else:
            Printer.Print("The array is not of numeric type so cannot",
                          "take mean")

        return result_object

    def ArgNotFoundResponse(self, arg_name):
        super().AnalyzeArgNotFoundResponse(arg_name)

    def MultipleArgsFoundResponse(self, arg_name):
        super().AnalyzeMultipleArgsFoundResponse(arg_name)
