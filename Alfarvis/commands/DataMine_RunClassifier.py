#!/usr/bin/env python
"""
Run a trained classifier on a group of arrays
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


class DM_Classify(AbstractCommand):
    """
    Run a trained classifier on a bunch of arrays
    """

    def briefDescription(self):
        return "run trained classifier on a bunch of arrays"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the train a classifier command
        """
        return ["classify", "classifier", "run"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the run classifier command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1),
                         Argument(keyword="classifier_model", optional=True,
                         argument_type=DataType.trained_model)]

    def evaluate(self, array_datas, classifier_model):
        """
        Run a trained classifier on multiple arrays

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        # Get the data frame
        sns.set(color_codes=True)
        command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        if StatContainer.ground_truth is None:
            Printer.Print("Please set a feature vector to ground truth by",
                          "typing set ground truth to",
                          "to get the prediction accuracy")
            result_object = ResultObject(None, None, None, CommandStatus.Error)
            return result_object
        else:
            df = DataGuru.removeGT(df, StatContainer.ground_truth)
            Y = StatContainer.ground_truth.data

        # Remove nans:
        df, Y = DataGuru.removenan(df, Y)
        X = df.values

        # Get the classifier model
        trained_model = classifier_model.data
        model = trained_model['Model']
        scaler = trained_model['Scaler']

        # Scale the values based on the training standardizer
        X = scaler.transform(X)

        # Code to run the classifier
        # Plot the k -means result
        Printer.Print('Running the trained classifier...')

        predictions = model.predict(X)
        accuracy = metrics.accuracy_score(predictions, Y)
        Printer.Print("Accuracy : %s" % "{0:.3%}".format(accuracy))
        cm = metrics.confusion_matrix(Y, predictions)
        DataGuru.plot_confusion_matrix(cm, np.unique(Y), title="confusion matrix")
        plt.show(block=False)

        # TODO Need to save the model
        # Ask user for a name for the model
        result_object = ResultObject(None, None, None, CommandStatus.Success)

        return result_object
