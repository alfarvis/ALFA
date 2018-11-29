#!/usr/bin/env python
"""
Concatenate multiple arrays to form a dataframe
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.Toolboxes.DataGuru import DataGuru
from Alfarvis.printers import Printer, TablePrinter


class ConcatenateArrays(AbstractCommand):
    """
    Concatenate multiple arrays into a dataframe
    """

    def briefDescription(self):
        return "concatenate arrays into a dataframe"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        Tags to identify the concatenate
        """
        return ["concatenate", "concatenate arrays", "combine arrays"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the concatenate array command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Create a a new dataframe using the supplied arrays

        """
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas)
        if command_status == CommandStatus.Error:
            Printer.Print("Please check whether the arrays are of the same size")
            return ResultObject(None, None, None, CommandStatus.Error)

        result_object = ResultObject(df, [], DataType.csv,
                              CommandStatus.Success)

        command_name = 'concatenate.array'
        result_object.createName(cname, command_name=command_name,
                          set_keyword_list=True)

        TablePrinter.printDataFrame(df)

        return result_object

    def ArgNotFoundResponse(self, file_name):
        super().ArgNotFoundResponse(file_name, 'variable(s)', 0)

    def MultipleArgsFoundResponse(self, file_name):
        super().MultipleArgsFoundResponse(file_name, 'variables', 0)
