#!/usr/bin/env python
"""
Find the best classifier using k fold cross validation
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


class DM_BestClassifier(AbstractCommand):
    """
    Find the best classifier using k fold cross validation
    """

    def briefDescription(self):
        return "find best classifier among specified classifiers"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the train a classifier command
        """
        return ["best classifier", "top classifier"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the train classifier command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1),
                         Argument(keyword="classifier_algos", optional=True,
                         argument_type=DataType.algorithm_arg, number=-1)]

    def evaluate(self, data_frame, classifier_algos):
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

        Printer.Print("Training classifier using the following features:")
        Printer.Print(df.columns)

        # Get all the classifier models to test against each other
        modelList = []
        Printer.Print("Testing the following classifiers: ")
        for classifier_algo in classifier_algos:
            model = (classifier_algo.data)
            Printer.Print(classifier_algo.name)
            modelList.append({'Name': classifier_algo.name, 'Model': model})

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        Printer.Print('Finding the best classifier using',
                      'k fold cross validation...')

        all_cv_scores, all_mean_cv_scores, all_confusion_matrices = DataGuru.FindBestClassifier(X, Y, modelList, 10)
        
        Printer.Print('\n\nPlotting the confusion matrices...\n')
        for iter in range(len(modelList)):
            win = Window.window()
            f = win.gcf()
            ax = f.add_subplot(111)
            DataGuru.plot_confusion_matrix(all_confusion_matrices[iter], np.unique(Y), ax,title=modelList[iter]['Name'])
            win.show()

        Printer.Print("\n\nBest classifier is " + modelList[np.argmax(all_mean_cv_scores)]['Name'] + " with an accuracy of -  %.2f%% " % max(all_mean_cv_scores))
        # TODO Need to save the model
        # Ask user for a name for the model
        result_object = ResultObject(None, None, None, CommandStatus.Success)

        return result_object
