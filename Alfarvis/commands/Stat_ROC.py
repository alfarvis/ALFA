#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define ROC calculator command

Created on Thu Mar  8 00:33:34 2018

@author: vishwaparekh
"""
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .argument import Argument
from .abstract_command import AbstractCommand
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer, TablePrinter
import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
class StatROC(AbstractCommand):
    """
    Calculates ROC for a predictor variable
    """

    def briefDescription(self):
        return "calculate ROC for an array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def commandName(self):
        return "statistics.roc"

    def commandTags(self):
        """
        return tags that are used to identify ROC command
        """
        return ["roc", "auc"]

    def argumentTypes(self):
        """
        A list of  argument objects that specify the inputs needed for
        executing the ROC command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1, fill_from_cache=False), 
                Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1, fill_from_cache=False)]

    def evaluate(self, array_datas,data_frame):
        """
        Calculate ROC of the array and store it to history
        Parameters:

        """
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

        if StatContainer.ground_truth is None:
            Printer.Print("Could not find the reference variable.")
            Printer.Print("Please set the reference variable")
            return ResultObject(None, None, None, CommandStatus.Error)
        else:
            gtVals = StatContainer.filterGroundTruth()
            ground_truth = StatContainer.ground_truth.name
            if len(gtVals) != df.shape[0]:
                Printer.Print("The size of the ground truth does not match with arrays being analyzed")
                Printer.Print(len(gtVals), df.shape[0])
                return ResultObject(None, None, None, CommandStatus.Error)
        
        uniqVals = StatContainer.isCategorical(gtVals)
        df[ground_truth] = gtVals
        df_new = pd.DataFrame()
        if ground_truth in df.columns:
            df_new['features'] = df.columns.drop(ground_truth).values
        else:
            df_new['features'] = df.columns
        
        allCols = df_new['features']
        for iter in range(len(uniqVals)):
            for iter1 in range(iter+1,len(uniqVals)):
                df_new['AUC'] = 0
                    
        avgAUC = []
        for iter_feature in range(len(df_new['features'])):
            arr = df[allCols[iter_feature]]
            model = LogisticRegression()
            X = arr.values
            X1 = X.reshape(-1,1)
            model.fit(X1, gtVals)
            # evaluate the model            
            allAUC = []
            Y_Pr = model.predict_proba(X1)           
            for iter in range (len(uniqVals)):
                fpr, tpr, thresholds = metrics.roc_curve(gtVals, Y_Pr[:, iter], pos_label=uniqVals[iter])
                fpr, tpr, thresholds = metrics.roc_curve(gtVals, Y_Pr[:, iter], pos_label=uniqVals[iter])
                auc_val = metrics.auc(fpr, tpr)
                allAUC.append(auc_val)
            avgAUC.append(np.mean(allAUC))
        df_new['AUC'] = avgAUC
                    
                        
        TablePrinter.printDataFrame(df_new)
        
        # New data frame
        result_objects = []
        result_object = ResultObject(df_new, [], DataType.csv,
                              CommandStatus.Success)
        result_object.createName(cname, command_name='rcurve',
                          set_keyword_list=True)
        
        result_objects.append(result_object)
        
        # create an updated list of column names by removing the common names
        kl1 = df_new.columns
        truncated_kl1, common_name = StatContainer.removeCommonNames(kl1)
        for col in range (0,len(kl1)):
            arr = df_new[kl1[col]]
            result_object = ResultObject(arr, [], DataType.array,
                              CommandStatus.Success)
            command_name = 'rcurve'
            result_object.createName(truncated_kl1[col], command_name=command_name,
                      set_keyword_list=True)

            result_objects.append(result_object)
        
        return result_objects
    
    def ArgNotFoundResponse(self,arg_name):
        Printer.Print("Which variable(s) do you want me to analyze?")
    
    def ArgFoundResponse(self,arg_name):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, arg_name):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to analyze?")