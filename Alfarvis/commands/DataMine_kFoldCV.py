#!/usr/bin/env python
"""
Run k fold cross validation using a classifier
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
import pandas as pd
from sklearn.manifold import TSNE
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import metrics # for the check the error and accuracy of the model
from sklearn import preprocessing

class DM_TrainClassifier(AbstractCommand):
    """
    Run k fold CV on a bunch of arrays
    """

    def commandTags(self):
        """
        Tags to identify the train a classifier command
        """
        return ["cv","cross","validation","fold"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the train classifier command
        """
        #TODO Add an argument for k = number of clusters
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1), 
                         Argument(keyword="classifier_algo", optional=True,
                         argument_type=DataType.algorithm_arg)]

    def evaluate(self, array_datas, classifier_algo):
        """
        Train a classifier on multiple arrays

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        
        # Get the data frame
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        
        #remove ground truth from data
        if StatContainer.ground_truth is not None:
            df = DataGuru.removeGT(df,StatContainer.ground_truth)
        # Get the classifier model
        model = classifier_algo.data
        
        #Code to run the classifier
        X = df.values
        
        #Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)
        
        #Get the ground truth array
        if StatContainer.ground_truth is None:
            print("Please set a feature vector to ground truth by typing set ground truth before using this command")
            result_object = ResultObject(None, None, None, CommandStatus.Error)
            return result_object
        else:
            Y = StatContainer.ground_truth.data
        model.fit(X, Y)
        
        
        
        print('Running k fold cross validation...')
        
        
        DataGuru.runKFoldCV(X,Y,model,10)
    
        
        #TODO Need to save the model
        #Ask user for a name for the model
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
