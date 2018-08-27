#!/usr/bin/env python
"""
Plot a scatter plot between two arrays
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.Toolboxes.DataGuru import DataGuru
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
import numpy as np


class StatDiff(AbstractCommand):
    """
    subtract two arrays
    """

    def briefDescription(self):
        return "subtract array1 from array2"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def commandTags(self):
        """
        Tags to identify the scatterplot command
        """
        return ["subtract", "-"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the scatter plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=2)]

    def evaluate(self, array_datas):
        """
        Create a scatter plot between two variables

        """
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas)
        if command_status == CommandStatus.Error:
            Printer.Print("please try the following command:",
                          "subtract a from b")
            return ResultObject(None, None, None, CommandStatus.Error)
        df_array = df.as_matrix()
        try:
            out = df_array[:, 1] - df_array[:, 0]
        except:
            return ResultObject(None, None, None, CommandStatus.Error)
        result_object = ResultObject(out, [],
                                     DataType.array,
                                     CommandStatus.Success)
        result_object.createName(
                array_datas[0].keyword_list,
                command_name=self.commandTags()[0],
                set_keyword_list=True)
        return result_object
