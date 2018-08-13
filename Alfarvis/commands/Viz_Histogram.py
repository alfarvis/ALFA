#!/usr/bin/env python
"""
Plot multiple arrays on a histogram
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
from Alfarvis.windows import Window
import seaborn as sns
import numpy as np
from Alfarvis.Toolboxes.DataGuru import DataGuru
from .Viz_Container import VizContainer


class VizHistogram(AbstractCommand):
    """
    Plot multiple array histograms on a single plot
    """
    max_unique = 50

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

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
        dCol = df[df.columns[0]]
        try:
            uniqVals, inv, counts = np.unique(
                dCol, return_inverse=True, return_counts=True)
        except:
            return ResultObject(None, None, None, CommandStatus.Error)
        if len(uniqVals) > self.max_unique:
            if isinstance(uniqVals[0], str):
                best_idx = np.argpartition(
                        counts, -self.max_unique)[-self.max_unique:]
                idx = np.isin(inv, best_idx)
                dCol = dCol[idx]
            else:
                uniqVals = None
        if uniqVals is not None and isinstance(uniqVals[0], str):
            max_len = max([len(uniqVal) for uniqVal in uniqVals])
        else:
            max_len = 0

        if (uniqVals is None and
            not np.issubdtype(dCol.dtype, np.number)):
            Printer.Print("Too many unique values in non-numeric type data")
            return ResultObject(None, None, None, CommandStatus.Error)

        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)

        # TODO Create an argument for setting number of bins
        if uniqVals is not None:
            if len(uniqVals) > 5 and max_len > 8:
                df = dCol.to_frame(name=kl1[0])
                sns.countplot(y=kl1[0], data=df, ax=ax)
            else:
                df = dCol.to_frame(name=kl1[0])
                sns.countplot(x=kl1[0], data=df, ax=ax)
        elif np.issubdtype(dCol.dtype, np.number):
            df.plot.hist(stacked=True, bins=20, ax=ax)

        win.show()

        return VizContainer.createResult(win, array_datas, ['histogram', 'hist'])
