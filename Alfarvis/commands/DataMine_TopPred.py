#!/usr/bin/env python
"""
Identify the top predictors in a dataset
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern,
                                        findNumbers, searchDateTime)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
import pandas as pd
from sklearn.manifold import TSNE
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import metrics  # for the check the error and accuracy of the model
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier


class DM_topPredictor(AbstractCommand):
    """
    Find top N predictors
    """

    def briefDescription(self):
        return "find top N predictors in a dataset"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the "Find top predictors" command
        """
        return ["top predictor"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the find top predictors command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="data_frame", optional=False,
                         argument_type=DataType.csv, number=1),
                         Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, data_frame, target):
        """
        Use one of the models to identify the top predictors
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        # Get the data frame
        df = data_frame.data
        #command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)

        if StatContainer.ground_truth is None:
            Printer.Print("Please set a feature vector to ground truth by",
                          "typing set ground truth before using this command")
            result_object = ResultObject(None, None, None, CommandStatus.Error)
            return result_object
        else:
            df = DataGuru.removeGT(df, StatContainer.ground_truth)
            Y = StatContainer.filterGroundTruth()

        # Remove nans:
        df, Y = DataGuru.removenan(df, Y)

        numbers = findNumbers(target.data, 1)
        if numbers != [] and numbers[0].data > 0:
            num = int(numbers[0].data)
        else:
            num = 10  # If not specified select top 10 features

        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, Y)
        featImpVals = model.feature_importances_

        featimp = pd.Series(featImpVals, index=df.columns).sort_values(ascending=False)
        Printer.Print("Here is the sorted list of top features: ")
        Printer.Print(featimp)

        df_new = df[featimp.index[0:num]]

        result_object = ResultObject(df_new, [], DataType.csv,
                              CommandStatus.Success)

        command_name = 'top.predictors'
        result_object.createName(data_frame.name, command_name=command_name,
                          set_keyword_list=True)

        return result_object
