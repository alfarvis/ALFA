#!/usr/bin/env python
"""
Create a pie plot with multiple categories
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Viz_Container import VizContainer
from .Stat_Container import StatContainer
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class VizPiePlots(AbstractCommand):
    """
    Plot multiple categories on a single pie plot with error bars
    """

    def commandTags(self):
        """
        Tags to identify the pie plot command
        """
        return ["pie", "chart", "plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the pie plot command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Create a pie plot 

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        stTitle = " ".join(array_data.keyword_list)
        if StatContainer.conditional_array is not None:
            inds = StatContainer.conditional_array.data
            print("Nfiltered: ", np.sum(inds))
        else:
            inds = np.full(array_data.data.size, True)
        col_data = pd.Series(array_data.data[inds])
        col_data.dropna(inplace=True)
        uniqVals = StatContainer.isCategorical(col_data)
        if uniqVals is not None:
            freq_vals = []
            for uniQ in uniqVals:
                ind = (col_data.values == uniQ)
                freq_vals.append(np.sum(ind * 1))
        else:
            print("Too many unique values to plot on a pie chart\n")
            print("Please select another chart type")
            return result_object

        df = pd.Series(freq_vals, index=uniqVals, name='')

        f = plt.figure()
        ax = f.add_subplot(111)

        df.plot.pie(figsize=(8, 8), ax=ax)
        ax.set_title(stTitle)
        ax.set_xlabel('')

        plt.show(block=False)
        return VizContainer.createResult(f, array_data, ['pie'])
