#!/usr/bin/env python
"""
Train a classifier on a group of arrays
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
from sklearn.manifold import TSNE
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import metrics  # for the check the error and accuracy of the model
from sklearn import preprocessing


class DM_TrainClassifier(AbstractCommand):
    """
    Train a classifier on a bunch of arrays
    """

    def briefDescription(self):
        return "train classifier on a dataset"

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

        return [Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1),
                         Argument(keyword="classifier_algo", optional=True,
                         argument_type=DataType.algorithm_arg)]

    def evaluate(self, data_frame, classifier_algo):
        """
        Train a classifier on multiple arrays

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

        # Get the classifier model
        model = classifier_algo.data[0]

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        # Train the classifier
        Printer.Print("Training the classifier")
        df_show = pd.DataFrame()
        df_show['Features'] = df.columns

        TablePrinter.printDataFrame(df_show)
        model.fit(X, Y)

        # Print an update
        Printer.Print("The classifier", classifier_algo.name,
                      "has been trained")

        predictions = model.predict(X)
        accuracy = metrics.accuracy_score(predictions, Y)
        Printer.Print("Accuracy on training set : %s" % "{0:.3%}".format(accuracy))

        trained_model = {'Scaler': scaler, 'Model': model}

        result_object = ResultObject(trained_model, [], DataType.trained_model,
                              CommandStatus.Success)

        classifier_algo_name = classifier_algo.name.replace('.', ' ')
        result_object.createName(data_frame.keyword_list, command_name=classifier_algo_name,
                          set_keyword_list=True)

        return result_object
