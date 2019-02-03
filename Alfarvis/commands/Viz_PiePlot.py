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
from Alfarvis.printers import Printer
from Alfarvis.windows import Window
import numpy as np
import seaborn as sns
import pandas as pd


class VizPiePlots(AbstractCommand):
    """
    Plot multiple categories on a single pie plot with error bars
    """
    max_unique = 50

    def briefDescription(self):
        return "pie plot of an array"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandName(self):
        return "visualization.pieplot"

    def commandTags(self):
        """
        Tags to identify the pie plot command
        """
        return ["pie plot", "pie chart", "plot"]

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
        if StatContainer.conditional_array is not None and len(StatContainer.conditional_array.data) == array_data.data.size:
            inds = StatContainer.conditional_array.data
            Printer.Print("Nfiltered: ", np.sum(inds))
        else:
            inds = np.full(array_data.data.size, True)
        col_data = pd.Series(array_data.data[inds], name='array')
        col_data.dropna(inplace=True)
        try:
            uniqVals, inv, counts = np.unique(
                col_data, return_inverse=True, return_counts=True)
        except:
            return ResultObject(None, None, None, CommandStatus.Error)
        if len(uniqVals) > self.max_unique:
            if isinstance(uniqVals[0], str):
                best_idx = np.argpartition(
                        counts, -self.max_unique)[-self.max_unique:]
                idx = np.isin(inv, best_idx)
                col_data = col_data[idx]
            elif np.issubdtype(col_data.dtype, np.number):
                # Convert to categorical
                col_data = pd.cut(col_data, 10)
                uniqVals = True
            else:
                uniqVals = None

        if uniqVals is not None:
            counts = pd.Series(np.ones(col_data.size), name='count')
            concat_df = pd.concat([counts, col_data], axis=1)
            ds = concat_df.groupby(col_data.name).sum()['count']
        else:
            Printer.Print("Too many unique values to plot on a pie chart\n")
            Printer.Print("Please select another chart type")
            return result_object

        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)

        ds.plot.pie(figsize=(8, 8), ax=ax)
        ax.set_title(stTitle)
        ax.set_xlabel('')
        ax.set_aspect('equal')

        win.show()
        return VizContainer.createResult(win, array_data, ['pie'])
