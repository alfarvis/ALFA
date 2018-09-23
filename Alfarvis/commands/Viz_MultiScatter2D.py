#!/usr/bin/env python
"""
Plot multiple arrays in a multidimensional scatterplot
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
import pandas as pd
from Alfarvis.Toolboxes.DataGuru import DataGuru
from .Viz_Container import VizContainer
from Alfarvis.windows import Window


class VizMultiScatter2D(AbstractCommand):
    """
    Plot multiple arrays against each other in a multidimensional scatterplot
    """

    def briefDescription(self):
        return "Plot multiple arrays against each other in a multidimensional scatterplot"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandTags(self):
        """
        Tags to identify the multidimensional scatterplot command
        """
        return ["multiscatterplot", "multi scatterplot", "multi scatter", "plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the multiscatter command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Create a scatter plot between multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)

        if StatContainer.ground_truth is None or len(StatContainer.ground_truth.data) != df.shape[0]:
            df.dropna(inplace=True)
            pd.plotting.scatter_matrix(df, alpha=0.2, diagonal='kde', ax=ax)
        else:
            gt1 = pd.Series(StatContainer.filterGroundTruth())
            df, gt1 = DataGuru.removenan(df, gt1)
            lut = dict(zip(gt1.unique(), np.linspace(0, 1, gt1.unique().size)))
            row_colors = gt1.map(lut)
            pd.plotting.scatter_matrix(df, alpha=0.2, diagonal='kde', c=row_colors, cmap="jet", ax=ax)

        f.suptitle(cname)

        win.show()

        return VizContainer.createResult(win, array_datas, ['multiscatter'])
