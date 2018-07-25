#!/usr/bin/env python
"""
Compute Correlation between 2 or more arrays
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
from .Viz_Container import VizContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru
from Alfarvis.printers import Printer


class Stat_Correl(AbstractCommand):
    """
    Compute Correlation between 2 or more arrays
    """

    def commandTags(self):
        """
        Tags to identify the correlation command
        """
        return ["correlation", "correlate"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the correlation command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Find the correlation between two or more variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        if len(array_datas) < 2:
            Printer.Print("Need atleast two arrays to compute correlation")
            return ResultObject(None, None, None, CommandStatus.Error)

        sns.set(color_codes=True)
        command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(
                array_datas, remove_nan=True)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        corr_res = df.corr()

        if len(array_datas) == 2:
            Printer.Print("The correlation between ", kl1[0], " and ", kl1[1],
                          " is ", str(corr_res.values[0][1]))

        Printer.Print("Displaying the result as a heatmap")
        f = plt.figure()
        ax = f.add_subplot(111)
        sns.heatmap(corr_res, cbar=True, square=True, annot=True, fmt='.2f',
                    annot_kws={'size': 15},
                    xticklabels=df.columns, yticklabels=df.columns,
                    cmap='jet', ax=ax)
        plt.show(block=False)
        return VizContainer.createResult(f, array_datas, ['correlation'])
