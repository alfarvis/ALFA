#!/usr/bin/env python
"""
Plot multiple arrays in a single line plot
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
from Alfarvis.windows import Window
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Alfarvis.Toolboxes.DataGuru import DataGuru
from .Stat_Container import StatContainer
from .Viz_Container import VizContainer


class VizPlotLine(AbstractCommand):
    """
    Plot multiple arrays in a single line plot
    """

    def briefDescription(self):
        return "line plot of an array"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandTags(self):
        """
        Tags to identify the lineplot command
        """
        return ["lineplot", "line plot", "plot", "plot line"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the lineplot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Create a line plot 

        """
        sns.set(color_codes=True)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas, useCategorical=True, expand_single=True,
                remove_nan=True)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        elif (df.shape[0] == 0 or
              (df.shape[1] == 1 and
               np.issubdtype(array_datas[0].data.dtype, np.number) == False)):
            Printer.Print("No data left to plot after cleaning up!")
            return ResultObject(None, None, None, CommandStatus.Error)

        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)
        ax.set_title(cname)
        df.plot(ax=ax)

        win.show()

        return VizContainer.createResult(win, array_datas, ['line'])
