#!/usr/bin/env python
"""
Plot multiple arrays on a violin plot
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


class Viz_VioloinPlot(AbstractCommand):
    """
    Plot multiple arrays on a violin plot
    """

    def briefDescription(self):
        return "violin plot of multiple arrays"

    def commandName(self):
        return "visualization.violinplot"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandTags(self):
        """
        Tags to identify the violin command
        """
        return ["violin plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the violin plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Create a violin plot for multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        sns.set(color_codes=True)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas, remove_nan=True)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)
        if StatContainer.ground_truth is None or len(StatContainer.ground_truth.data) != df.shape[0]:
            df.dropna(inplace=True)
            sns.violinplot(data=df, ax=ax)
        else:
            ground_truth = " ".join(StatContainer.ground_truth.keyword_list)
            df[ground_truth] = StatContainer.filterGroundTruth()
            df.dropna(inplace=True)
            df1 = pd.melt(df, id_vars=ground_truth)
            sns.violinplot(data=df1, ax=ax, x='variable', y='value', hue=ground_truth)

        win.show()

        return VizContainer.createResult(win, array_datas, ['violin'])
