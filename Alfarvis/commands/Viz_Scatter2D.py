#!/usr/bin/env python
"""
Plot a scatter plot between two arrays
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru
import pandas as pd
from .Viz_Container import VizContainer


class VizScatter2D(AbstractCommand):
    """
    Plot two arrays against each other in a scatterplot
    """

    def commandTags(self):
        """
        Tags to identify the scatterplot command
        """
        return ["scatterplot", "scatter plot"]

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
        sns.set(color_codes=True)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        f = plt.figure()
        ax = f.add_subplot(111)
        if StatContainer.ground_truth is None:
            df.dropna(inplace=True)
            if df.shape[0] == 0:
                return ResultObject(None, None, None, CommandStatus.Error)
            array = df.values
            plt.scatter(array[:, 0], array[:, 1], edgecolor="None", alpha=0.35)
        else:
            gt1 = pd.Series(StatContainer.filterGroundTruth())
            df, gt1 = DataGuru.removenan(df, gt1)
            if df.shape[0] == 0:
                return ResultObject(None, None, None, CommandStatus.Error)
            lut = dict(zip(gt1.unique(), np.linspace(0, 1, gt1.unique().size)))
            row_colors = gt1.map(lut)
            array = df.values
            ax.scatter(array[:, 0], array[:, 1], c=row_colors, cmap="jet",
                       edgecolor="None", alpha=0.35)
        ax.set_xlabel(kl1[0])
        ax.set_ylabel(kl1[1])
        ax.set_title(cname)
        plt.show(block=False)

        return VizContainer.createResult(f, array_datas, ['scatter2d'])
