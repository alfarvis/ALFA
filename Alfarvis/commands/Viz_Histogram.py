#!/usr/bin/env python
"""
Plot multiple arrays on a histogram
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from .Stat_Container import StatContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru
from .Viz_Container import VizContainer


class VizHistogram(AbstractCommand):
    """
    Plot multiple array histograms on a single plot
    """

    def commandTags(self):
        """
        Tags to identify the histogram command
        """
        return ["histogram", "frequency plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the histogram command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def evaluate(self, array_datas):
        """
        Create a histogram for multiple variables

        """

        sns.set(color_codes=True)
        command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(
                array_datas, useCategorical=True, remove_nan=True)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        uniqVals = StatContainer.isCategorical(df[df.columns[0]])
        if uniqVals is not None and isinstance(uniqVals[0], str):
            max_len = max([len(uniqVal) for uniqVal in uniqVals])
        else:
            max_len = 0

        if (uniqVals is None and
            not np.issubdtype(df[df.columns[0]].dtype, np.number)):
            print("Too many unique values in non-numeric type data")
            return ResultObject(None, None, None, CommandStatus.Error)

        f = plt.figure()
        ax = f.add_subplot(111)

        # TODO Create an argument for setting number of bins
        if uniqVals is not None:
            if len(uniqVals) > 5 and max_len > 8:
                sns.countplot(y=kl1[0], data=df, ax=ax)
            elif uniqVals is n:
                sns.countplot(x=kl1[0], data=df, ax=ax)
        elif np.issubdtype(df[df.columns[0]].dtype, np.number):
            df.plot.hist(stacked=True, bins=20, ax=ax)

        plt.show(block=False)

        return VizContainer.createResult(f, array_datas, ['histogram', 'hist'])
