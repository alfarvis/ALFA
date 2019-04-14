#!/usr/bin/env python
"""
Plot a scatter plot between two arrays
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.windows import Window
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru
import pandas as pd
from .Viz_Container import VizContainer
from Alfarvis.printers import Printer
from .modify_figure import ModifyFigure
from mpl_toolkits.axes_grid1 import make_axes_locatable


class VizScatter2D(AbstractCommand):
    """
    Plot two arrays against each other in a scatterplot
    """
    modify_figure = ModifyFigure()

    def briefDescription(self):
        return "scater2d plot of an array"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandTags(self):
        """
        Tags to identify the scatterplot command
        """
        return ["scatterplot", "scatter plot", "scatter 2d", "scatter", "plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the scatter plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=2)]

    def createDefaultProperties(self):
        properties = {}
        properties["invert"] = False
        properties["add_regression_line"] = False
        properties["add_data_distribution"] = False
        return properties

    def evaluate(self, array_datas):
        """
        Create a scatter plot between two variables

        """
        sns.set(color_codes=True)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
            array_datas)
        if command_status == CommandStatus.Error:
            Printer.Print("please try the following command:",
                          "Visualize comparison between...")
            return ResultObject(None, None, None, CommandStatus.Error)

        properties = self.createDefaultProperties()
        properties['title'] = cname

        win = Window.window()
        row_colors = None
        if StatContainer.ground_truth is None or len(StatContainer.ground_truth.data) != df.shape[0]:
            df.dropna(inplace=True)
            if df.shape[0] == 0:
                return ResultObject(None, None, None, CommandStatus.Error)
            array = df.values
        else:
            gt1 = pd.Series(StatContainer.filterGroundTruth())
            df, gt1 = DataGuru.removenan(df, gt1)
            if df.shape[0] == 0:
                return ResultObject(None, None, None, CommandStatus.Error)
            lut = dict(zip(gt1.unique(), np.linspace(0, 1, gt1.unique().size)))
            row_colors = gt1.map(lut)
            array = df.values

        result_object = VizContainer.createResult(
            win, array_datas, ['scatter2d'])
        result_object.data = [win, properties, [
            array, row_colors, kl1], self.updateFigure]
        self.updateFigure(result_object.data)
        self.modify_figure.evaluate(result_object)
        return result_object

    def updateFigure(self, result_data):
        win = result_data[0]
        f = win.gcf()
        f.clear()
        ax = f.add_subplot(111)
        properties = result_data[1]
        data = result_data[2]
        array = data[0]
        row_colors = data[1]
        kl1 = data[2]
        if properties["invert"]:
            array[:, [0, 1]] = array[:, [1, 0]]
            kl1[0], kl1[1] = kl1[1], kl1[0]

        if row_colors is None:
            ax.scatter(array[:, 0], array[:, 1], edgecolor="None", alpha=0.35)
        else:

            sc = ax.scatter(array[:, 0], array[:, 1], c=row_colors, cmap="jet",
                            edgecolor="None", alpha=0.35)

            cbar = plt.colorbar(sc)
            cbar.ax.get_yaxis().labelpad = 15
            cbar.ax.set_ylabel(StatContainer.ground_truth.name, rotation=270)

        ax.set_xlabel(kl1[0])
        ax.set_ylabel(kl1[1])
        ax.set_title(properties["title"])

        if properties["add_data_distribution"]:

            divider = make_axes_locatable(ax)
            axHistx = divider.append_axes("top", 1.1, pad=0.1, sharex=ax)
            axHisty = divider.append_axes("right", 1.1, pad=0.1, sharey=ax)
            # make some labels invisible
            axHistx.xaxis.set_tick_params(labelbottom=False)
            axHisty.yaxis.set_tick_params(labelleft=False)

            axHistx.hist(array[:, 0])
            axHisty.hist(array[:, 1], orientation='horizontal')

        if properties["add_regression_line"]:
            m, b = np.polyfit(array[:, 0], array[:, 1], 1)
            X_plot = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 100)
            ax.plot(X_plot, m * X_plot + b, '-')
