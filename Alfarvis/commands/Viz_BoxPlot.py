#!/usr/bin/env python
"""
Plot multiple arrays as box plots
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


class VizMultiScatter2D(AbstractCommand):
    """
    Plot multiple arrays as box plots
    """

    def commandTags(self):
        """
        Tags to identify the box plot
        """
        return ["boxplot", "box", "plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the box plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Create a box plot between multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)
        f = plt.figure()
        ax = f.add_subplot(111)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        if StatContainer.ground_truth is None:
            df.boxplot(figsize=(10, 10), ax=ax)
        else:
            ground_truth = " ".join(StatContainer.ground_truth.keyword_list)
            df[ground_truth] = StatContainer.ground_truth.data
            df.boxplot(by=ground_truth, figsize=(10, 10), ax=ax)

        plt.show(block=False)

        return VizContainer.createResult(f, array_datas, ['box'])
