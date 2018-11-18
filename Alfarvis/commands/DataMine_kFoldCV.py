#!/usr/bin/env python
"""
Run k fold cross validation using a classifier
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
from Alfarvis.windows import Window


class DM_TrainClassifier(AbstractCommand):
    """
    Run k fold CV on a bunch of arrays
    """

    def briefDescription(self):
        return "train classifier on a dataset"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the train a classifier command
        """
        return ["cv", "cross validation", "fold"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the train classifier command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1),
                         Argument(keyword="classifier_algo", optional=False,
                         argument_type=DataType.algorithm_arg)]

    def evaluate(self, data_frame, classifier_algo):
        """
        Train a classifier on multiple arrays

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        # Get the data frame
        sns.set(color_codes=True)
        df = data_frame.data
        #command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)
        #if command_status == CommandStatus.Error:
        #    return ResultObject(None, None, None, CommandStatus.Error)

        # Get the ground truth array
        if StatContainer.ground_truth is None:
            Printer.Print("Please set a feature vector to ground truth by",
                          "typing set ground truth before using this command")
            result_object = ResultObject(None, None, None, CommandStatus.Error)
            return result_object
        else:
            df = DataGuru.removeGT(df, StatContainer.ground_truth)
            Y = StatContainer.ground_truth.data

        # Remove nans:
        df, Y = DataGuru.removenan(df, Y)

        # Get the classifier model
        model = classifier_algo.data

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        Printer.Print('Running k fold cross validation...')

        cm, cvscores = DataGuru.runKFoldCV(X, Y, model, 10)
        win = Window.window()
        f = win.gcf()
        ax = f.add_subplot(111)
        DataGuru.plot_confusion_matrix(cm, np.unique(Y), ax, title="confusion matrix")
        win.show()

        # TODO Need to save the model
        # Ask user for a name for the model
        result_object = ResultObject(None, None, None, CommandStatus.Success)

        return result_object

    def ArgNotFoundResponse(self,arg_name):
        if arg_name=="data_frame":
            Printer.Print("Which data frame do you want me to classify?")
        else:
            Printer.Print("Which classifiers do you want me to test?")
    
    def ArgFoundResponse(self,arg_name):
        if arg_name=="data_frame":
            Printer.Print("Found the data frame") 
        else:
            Printer.Print("Found the classification models to test") 
        
    def MultipleArgsFoundResponse(self, arg_name):
        if arg_name == "data_frame":
            Printer.Print("I found multiple data frames that seem to match your query")
            Printer.Print("Could you please look at the following data frames and tell me which one you "
                  "want to classify?")
        
