#!/usr/bin/env python
"""
Create a bar plot with multiple variables
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
from Alfarvis.windows import Window
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
from .Viz_Container import VizContainer
import pandas as pd
from Alfarvis.Toolboxes.DataGuru import DataGuru
from .modify_figure import ModifyFigure


class VizBarPlots(AbstractCommand):
    """
    Plot multiple features on a single bar plot with error bars
    """
    modify_figure = ModifyFigure()

    def briefDescription(self):
        return "bar plot an array"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandTags(self):
        """
        Tags to identify the bar plot command
        """
        return ["bar", "plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the bar plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def createDefaultProperties(self):
        properties = {}
        properties["horizontal"] = False
        properties["overwrite_labels"] = False
        properties["ylabel"] = ''
        properties["xlabel"] = ''
        properties["title"] = ''
        properties["invert"] = False
        properties["color_map"] = "jet"
        properties["rotation"] = 0
        return properties

    def evaluate(self, array_datas):
        """
        Create a bar plot between multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
            array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        if StatContainer.ground_truth is None:
            gtVals = np.ones(df.shape[0])
            ground_truth = 'ground_truth'
        else:
            gtVals = StatContainer.filterGroundTruth()
            ground_truth = StatContainer.ground_truth.name
            if len(gtVals) != df.shape[0]:
                print("ground truth does not match with df shape")
                print(len(gtVals), df.shape[0])
                gtVals = np.ones(df.shape[0])
                ground_truth = 'ground_truth'

        # Remove nans:
        df[ground_truth] = gtVals
        df.dropna(inplace=True)
        gtVals = df[ground_truth]
        uniqVals = StatContainer.isCategorical(gtVals)
        binned_ground_truth = False
        if uniqVals is None and np.issubdtype(gtVals.dtype, np.number):
            # Convert to categorical
            df[ground_truth] = pd.cut(gtVals, 10)
            binned_ground_truth = True

        if binned_ground_truth is True or uniqVals is not None:
            gb = df.groupby(ground_truth)
            df_mean = gb.mean()
            df_errors = gb.std()
            if uniqVals is not None and isinstance(uniqVals[0], str):
                truncated_uniqVals, _ = StatContainer.removeCommonNames(
                        df_mean.index)
                df_mean.index = truncated_uniqVals
                df_errors.index = truncated_uniqVals
            # Number of uniq_vals x number of arrs
            df_mean_shape = df_mean.shape
            if (not binned_ground_truth and
                df_mean_shape[1] >= df_mean_shape[0]):
                df_mean = df_mean.T
                df_errors = df_errors.T
        else:
            Printer.Print("Ground truth could not be mapped to",
                          "categorical array\n")
            Printer.Print("Please clear or select appropriate ground truth")
            return result_object

        properties = self.createDefaultProperties()
        properties['title'] = cname
        if uniqVals is not None and isinstance(uniqVals[0], str):
            max_len = max([len(uniqVal) for uniqVal in uniqVals])
        else:
            max_len = 0
        if (binned_ground_truth or
            (uniqVals is not None and len(uniqVals) > 5 and max_len > 8)):
            properties["horizontal"] = True
        if binned_ground_truth:
            properties["overwrite_labels"] = True
            properties["ylabel"] = StatContainer.ground_truth.name
        win = Window.window()
        result_object = VizContainer.createResult(win, array_datas, ['bar'])
        result_object.data = [win, properties, [df_mean, df_errors], self.updateFigure]
        self.updateFigure(result_object.data,array_datas)
        self.modify_figure.evaluate(result_object)
        return result_object

    def updateFigure(self, result_data, array_datas):
        win = result_data[0]
        f = win.gcf()
        f.clear()
        ax = f.add_subplot(111)
        properties = result_data[1]
        data = result_data[2]
        if properties["invert"]:
            data[0] = data[0].T
            data[1] = data[1].T
        if properties["horizontal"]:
            data[0].plot.barh(xerr=data[1], cmap=properties["color_map"], ax=ax)
        else:
            data[0].plot.bar(yerr=data[1], cmap=properties["color_map"], ax=ax, rot=properties["rotation"])
        if properties["overwrite_labels"]:
            ax.set_xlabel(properties["xlabel"])
            ax.set_ylabel(properties["ylabel"])
        ax.set_title(properties["title"])
        win.show()
        return VizContainer.createResult(win, array_datas, ['bar'])

    def ArgNotFoundResponse(self, arg_name):
        super().AnalyzeArgNotFoundResponse(arg_name, 'plot')

    def MultipleArgsFoundResponse(self, arg_name):
        super().AnalyzeMultipleArgsFoundResponse(arg_name, 'plot')
