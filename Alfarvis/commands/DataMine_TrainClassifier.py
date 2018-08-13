#!/usr/bin/env python
"""
Train a classifier on a group of arrays
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
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


class DM_TrainClassifier(AbstractCommand):
    """
    Train a classifier on a bunch of arrays
    """

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the train a classifier command
        """
        return ["train", "classifier", "learn"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the train classifier command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1),
                         Argument(keyword="classifier_algo", optional=True,
                         argument_type=DataType.algorithm_arg)]

    def evaluate(self, array_datas, classifier_algo):
        """
        Train a classifier on multiple arrays

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        # Get the data frame
        sns.set(color_codes=True)
        command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

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

        # Get the classifier model
        model = classifier_algo.data

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        # Train the classifier
        Printer.Print("Training classifier using the following features:")
        Printer.Print(df.columns)
        model.fit(X, Y)

        # Print an update
        Printer.Print("The classifier", " ".join(classifier_algo.keyword_list),
                      "has been trained")

        predictions = model.predict(X)
        accuracy = metrics.accuracy_score(predictions, Y)
        Printer.Print("Accuracy on training set : %s" % "{0:.3%}".format(accuracy))
        plt.show(block=False)

        trained_model = {'Scaler': scaler, 'Model': model}

        # TODO Need to save the model
        # Ask user for a name for the model
        keyword_list = ["trained", "model"]
        keyword_list = keyword_list + classifier_algo.keyword_list

        result_object = ResultObject(trained_model, keyword_list, DataType.trained_model, CommandStatus.Success)

        return result_object
