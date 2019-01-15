#!/usr/bin/env python
"""
Visualize using pca
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
from sklearn.decomposition import PCA
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import preprocessing
from .Viz_Container import VizContainer


class NLDR_pca(AbstractCommand):
    """
    Visualize using pca
    """

    def briefDescription(self):
        return "visualize data using pca"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the pca command
        """
        return ["pca","principal component analysis"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the pca command
        """
        
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1, fill_from_cache=False), 
                Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1, fill_from_cache=False)]

    def evaluate(self, data_frame, array_datas):
        """
        Run pca on a dataset of multiple arrays

        """
        
        # Get the data frame        
        if data_frame is not None:
            df = data_frame.data
            df = DataGuru.convertStrCols_toNumeric(df)
            cname = data_frame.name
        elif array_datas is not None:
            command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas,useCategorical=True)
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

        # Train the classifier
        pca = PCA(n_components=2)
        pca_res = pca.fit_transform(X)
        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)
        
        if Y is None:
            sc = ax.scatter(pca_res[:, 0], pca_res[:, 1], cmap="jet",
                       edgecolor="None", alpha=0.35)
        else: 
            sc = ax.scatter(pca_res[:, 0], pca_res[:, 1], c=Y,cmap="jet",
                       edgecolor="None", alpha=0.35)
            cbar = plt.colorbar(sc)
            cbar.ax.get_yaxis().labelpad = 15
            cbar.ax.set_ylabel(StatContainer.ground_truth.name, rotation=270)

        ax.set_title(cname)
        win.show()
        #return ResultObject(None, None, None, CommandStatus.Success)
        
        if data_frame is not None:
            return VizContainer.createResult(win, data_frame, ['pca'])
        else:
            return VizContainer.createResult(win, array_datas, ['pca'])
