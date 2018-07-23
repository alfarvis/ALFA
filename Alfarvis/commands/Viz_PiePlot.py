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
        return ["pie chart", "pie plot"]

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
        col_data = pd.Series(array_data.data[inds], name='array')
        col_data.dropna(inplace=True)
        uniqVals = StatContainer.isCategorical(col_data)

        if uniqVals is None and np.issubdtype(col_data.dtype, np.number):
            # Convert to categorical
            col_data = pd.cut(col_data, 10)
            uniqVals = True

        if uniqVals is not None:
            counts = pd.Series(np.ones(col_data.size), name='count')
            concat_df = pd.concat([counts, col_data], axis=1)
            ds = concat_df.groupby(col_data.name).sum()['count']
        else:
            print("Too many unique values to plot on a pie chart\n")
            print("Please select another chart type")
            return result_object

        f = plt.figure()
        ax = f.add_subplot(111)

        ds.plot.pie(figsize=(8, 8), ax=ax)
        ax.set_title(stTitle)
        ax.set_xlabel('')

        plt.show(block=False)
        return VizContainer.createResult(f, array_data, ['pie'])
