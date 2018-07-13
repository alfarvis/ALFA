#!/usr/bin/env python
"""
Create a heatmap for visualization of the data
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
import pandas as pd


class Stat_Clustermap(AbstractCommand):
    """
    create a heatmap for data visualization
    """

    def commandTags(self):
        """
        Tags to identify the heatmap command
        """
        return ["heatmap", "clustermap"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the heatmap command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Displaying a heatmap for data visualization 

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        sns.set(color_codes=True)
        command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        print("Displaying heatmap")
        f = plt.figure()
        if StatContainer.ground_truth is None:
            sns.clustermap(df, cbar=True, square=False, annot=False,
                           cmap='jet', standard_scale=1)
        else:
            gt1 = pd.Series(StatContainer.ground_truth.data)
            lut = dict(zip(gt1.unique(), "rbg"))
            row_colors = gt1.map(lut)
            sns.clustermap(df, standard_scale=1, row_colors=row_colors,
                           cmap="jet")

        plt.show(block=False)
        return VizContainer.createResult(f, array_datas, ['heatmap'])
