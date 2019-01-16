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
        return [Argument(keyword="data_frame", optional=True, argument_type=DataType.csv, number=1, fill_from_cache=False),
                Argument(keyword="array_datas", optional=True,argument_type=DataType.array, number=-1, fill_from_cache=False),
                Argument(keyword="classifier_algo", optional=False, argument_type=DataType.algorithm_arg)]
    
    def createDefaultProperties(self):
        properties = {}
        properties["k (default: LOOCV)"] = "0"
        return properties
    
    def evaluate(self, data_frame, array_datas, classifier_algo):
        """
        Train a classifier on multiple arrays

        """
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
                return ResultObject(None, None, None, CommandStatus.Error)
        else: 
            Printer.Print("Please provide data frame or arrays to analyze")
            return ResultObject(None, None, None, CommandStatus.Error)
        #command_status, df, kl1, _ = DataGuru.transformArray_to_dataFrame(array_datas)
        # if command_status == CommandStatus.Error:
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
        model = classifier_algo.data[0]

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)
        
        properties = self.createDefaultProperties()
        properties['title'] = cname
        win = Window.window()
        
        if data_frame is not None:
            result_object =  VizContainer.createResult(win, data_frame, ['cval'])
        else:
            result_object = VizContainer.createResult(win, array_datas, ['cval'])

        
        result_object.data = [win, properties, [X,Y,model], self.updateFigure]
        self.updateFigure(result_object.data)
        self.modify_figure.evaluate(result_object)
        return result_object
        
        #cm, cvscores = DataGuru.runLOOCV(X, Y, model)
        #cm, cvscores = DataGuru.runKFoldCV(X, Y, model,2)
        
        
        #f = win.gcf()
        #ax = f.add_subplot(111)
        #DataGuru.plot_confusion_matrix(cm, np.unique(Y), ax, title="confusion matrix")
        #win.show()
    
    def updateFigure(self, result_data):
        win = result_data[0]
        f = win.gcf()
        f.clear()
        ax = f.add_subplot(111)
        properties = result_data[1]
        data = result_data[2]
        X = data[0]
        Y = data[1]
        model = data[2]
        try:
            kValue = int(properties["k (default: LOOCV)"])
            if kValue==0:
                Printer.Print("Using leave one out cross validation")
            else:
                Printer.Print("Using",kValue,"fold cross validation")
        except:
            Printer.Print("Using leave one out cross validation")
            kValue = 0
        
        if kValue > X.shape[0]:
            kValue = 0
            Printer.Print("k too high. Using leave one out cross validation")
        
        if kValue == 0:
            cm, cvscores = DataGuru.runLOOCV(X, Y, model)
        else:
            cm, cvscores = DataGuru.runKFoldCV(X, Y, model,kValue)
        DataGuru.plot_confusion_matrix(cm, np.unique(Y), ax, title="confusion matrix")
        ax.set_title(properties["title"])
        win.show()
    
    def ArgNotFoundResponse(self, arg_name):
        super().DataMineArgNotFoundResponse(arg_name)

    def ArgFoundResponse(self, arg_name):
        super().DataMineArgFoundResponse(arg_name)

    def MultipleArgsFoundResponse(self, arg_name):
        super().DataMineMultipleArgsFoundResponse(arg_name)
