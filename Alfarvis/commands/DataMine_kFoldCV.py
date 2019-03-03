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
from .Viz_Container import VizContainer
from .modify_figure import ModifyFigure


class DM_RunCrossValidation(AbstractCommand):
    """
    Run k fold CV on a bunch of arrays
    """
    modify_figure = ModifyFigure()

    def briefDescription(self):
        return "train classifier on a dataset"

    @property
    def run_in_background(self):
        return True

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the train a classifier command
        """
        return ["kfold cv", "cv", "cross validation", "fold"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the train classifier command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="data_frame", optional=True, argument_type=DataType.csv, number=1, fill_from_cache=False),
                Argument(keyword="array_datas", optional=True, argument_type=DataType.array, number=-1, fill_from_cache=False),
                Argument(keyword="classifier_algo", optional=False, argument_type=DataType.algorithm_arg)]

    def createDefaultProperties(self):
        properties = {}
        properties["k (default: LOOCV)"] = "0"
        return properties

    def preEvaluate(self, data_frame, array_datas, classifier_algo):
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        # Get the data frame
        sns.set(color_codes=True)
        if data_frame is not None:
            df = data_frame.data
            cname = data_frame.name
        elif array_datas is not None:
            command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas)
            if command_status == CommandStatus.Error:
                print("Error in getting dataframe!")
                result_object.data = "Error in getting dataframe!"
                return result_object
        else:
            result_object.data = "Please provide data frame or arrays to analyze"
            return result_object

        # Get the ground truth array
        if StatContainer.ground_truth is None:
            result_object.data = ("Please set a feature vector to ground truth by" +
                                  "typing set ground truth before using this command")
            return result_object
        else:
            df = DataGuru.removeGT(df, StatContainer.ground_truth)
            Y = StatContainer.ground_truth.data
        # Remove nans:
        df, Y = DataGuru.removenan(df, Y)

        # Get the classifier model
        model = classifier_algo.data[0]

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        properties = self.createDefaultProperties()
        properties['title'] = cname
        cv_output = self.performCV(properties, X, Y, model)
        aux_output = (properties, [X, Y, model])

        return [ResultObject(cv_output, None),
                ResultObject(aux_output, None)]

    def performCV(self, properties, X, Y, model):
        try:
            kValue = int(properties["k (default: LOOCV)"])
        except:
            kValue = 0
        if kValue > X.shape[0]:
            kValue = 0

        if kValue == 0:
            cm, cvscores = DataGuru.runLOOCV(X, Y, model)
        else:
            cm, cvscores = DataGuru.runKFoldCV(X, Y, model, kValue)
        return kValue, cm, cvscores

    def printkValueMessage(self, kValue):
        if kValue == 0:
            Printer.Print("Using leave one out cross validation")
        else:
            Printer.Print("Using", kValue, "fold cross validation")

    def evaluate(self, data_frame, array_datas, classifier_algo, pre_evaluate_results=None):
        """
        Train a classifier on multiple arrays

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if type(pre_evaluate_results) is not list:
            Printer.Print("Pre evaluation results failed! Attach bug report!")
            return result_object
        win = Window.window()

        if data_frame is not None:
            result_object = VizContainer.createResult(win, data_frame, ['cval'])
        elif array_datas is not None:
            result_object = VizContainer.createResult(win, array_datas, ['cval'])
        else:
            Printer.Print("Provide one of data frame or array datas")
            return result_object
        cv_output, aux_output = pre_evaluate_results
        properties, model_data = aux_output.data

        result_object.data = [win, properties, model_data, self.processkFoldCV]
        self.printkValueMessage(cv_output.data[0])
        self.updateWindow(win, cv_output.data[1], cv_output.data[2], model_data[1], properties["title"])
        self.modify_figure.evaluate(result_object)
        return result_object

    def updateWindow(self, win, cm, cvscores, Y, title):
        f = win.gcf()
        f.clear()
        ax = f.add_subplot(111)
        DataGuru.plot_confusion_matrix(cm, np.unique(Y), ax, title="confusion matrix")
        ax.set_title(title)
        win.show()

    def processkFoldCV(self, result_data):
        win = result_data[0]
        properties = result_data[1]
        data = result_data[2]
        X = data[0]
        Y = data[1]
        model = data[2]
        kValue, cm, cvscores = self.performCV(properties, X, Y, model)
        self.printkValueMessage(kValue)
        self.updateWindow(win, cm, cvscores, Y, properties["title"])

    def ArgNotFoundResponse(self, arg_name):
        super().DataMineArgNotFoundResponse(arg_name)

    def ArgFoundResponse(self, arg_name):
        super().DataMineArgFoundResponse(arg_name)

    def MultipleArgsFoundResponse(self, arg_name):
        super().DataMineMultipleArgsFoundResponse(arg_name)
