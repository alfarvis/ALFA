#!/usr/bin/env python
"""
Visualize using LLE
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer, TablePrinter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
import pandas as pd
from Alfarvis.windows import Window
from sklearn.manifold import LocallyLinearEmbedding
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import preprocessing
from .Viz_Container import VizContainer
from .modify_figure import ModifyFigure


class NLDR_LLE(AbstractCommand):
    """
    Visualize using LLE
    """
    modify_figure = ModifyFigure()

    def briefDescription(self):
        return "visualize data using LLE"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the LLE command
        """
        return ["lle", "locally linear embedding"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the LLE command
        """

        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1, fill_from_cache=False),
                Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1, fill_from_cache=False)]

    def createDefaultProperties(self):
        properties = {}
        properties["k"] = "20"
        return properties

    def evaluate(self, data_frame, array_datas):
        """
        Run LLE on a dataset of multiple arrays

        """

        # Get the data frame
        if data_frame is not None:
            df = data_frame.data
            df = DataGuru.convertStrCols_toNumeric(df)
            cname = data_frame.name
        elif array_datas is not None:
            command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas, useCategorical=True)
            if command_status == CommandStatus.Error:
                return ResultObject(None, None, None, CommandStatus.Error)
        else:
            Printer.Print("Please provide data frame or arrays to analyze")
            return ResultObject(None, None, None, CommandStatus.Error)
        Y = None
        if StatContainer.ground_truth is not None:
            df = DataGuru.removeGT(df, StatContainer.ground_truth)
            Y = StatContainer.filterGroundTruth()
            # Remove nans:
            df, Y = DataGuru.removenan(df, Y)
        else:
            df.dropna(inplace=True)

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        win = Window.window()

        properties = self.createDefaultProperties()
        properties['title'] = cname

        if data_frame is not None:
            result_object = VizContainer.createResult(win, data_frame, ['lle'])
        else:
            result_object = VizContainer.createResult(win, array_datas, ['lle'])

        result_object.data = [win, properties, [X, Y], self.updateFigure]
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
        X = data[0]
        Y = data[1]
        try:
            kValue = int(properties["k"])
        except:
            Printer.Print("Please enter an integer value for k.\n",
                          "Using default value of 20")
            kValue = 20

        if kValue > X.shape[0]:
            kValue = X.shape[0] - 1

        # Get the LLE model
        LLE_Train = LocallyLinearEmbedding(n_neighbors=kValue, n_components=2, method='standard')

        # Train the classifier
        lle_res = LLE_Train.fit_transform(X)
        if Y is None:
            sc = ax.scatter(lle_res[:, 0], lle_res[:, 1], cmap="jet",
                       edgecolor="None", alpha=0.35)
        else:
            sc = ax.scatter(lle_res[:, 0], lle_res[:, 1], c=Y, cmap="jet",
                       edgecolor="None", alpha=0.35)
            cbar = plt.colorbar(sc)
            cbar.ax.get_yaxis().labelpad = 15
            cbar.ax.set_ylabel(StatContainer.ground_truth.name, rotation=270)
        ax.set_title(properties["title"])
        win.show()
