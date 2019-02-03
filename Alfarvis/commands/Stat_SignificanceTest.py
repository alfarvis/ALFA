#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define ttest calculator command

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


class StatSigTest(AbstractCommand):
    """
    Calculates ttest for a predictor variable
    """

    def briefDescription(self):
        return "calculate ttest for an array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def commandTags(self):
        """
        return tags that are used to identify ttest command
        """
        return ["ttest", "p value", "t test"]

    def commandName(self):
        return "statistics.ttest"

    def argumentTypes(self):
        """
        A list of  argument objects that specify the inputs needed for
        executing the ttest command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1, fill_from_cache=False), 
                Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1, fill_from_cache=False)]

    def evaluate(self, array_datas,data_frame):
        """
        Calculate ttest of the array and store it to history
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
            print("Could not find the reference variable.")
            print("Please set the reference variable")
            return ResultObject(None, None, None, CommandStatus.Error)
        else:
            gtVals = StatContainer.filterGroundTruth()
            ground_truth = StatContainer.ground_truth.name
            if len(gtVals) != df.shape[0]:
                print("The size of the ground truth does not match with arrays being analyzed")
                print(len(gtVals), df.shape[0])
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
            for iter1 in range(iter + 1, len(uniqVals)):
                df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)] = np.zeros(df_new.shape[0])

        for iter_feature in range(len(df_new['features'])):
            arr = df[allCols[iter_feature]]
            for iter in range(len(uniqVals)):
                uniV = uniqVals[iter]
                a = arr[gtVals == uniV]
                for iter1 in range(iter + 1, len(uniqVals)):
                    b = arr[gtVals == uniqVals[iter1]]
                    if uniV != uniqVals[iter1]:
                        ttest_val = scipy.stats.ttest_ind(a, b, axis=0, equal_var=False)
                        df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)][iter_feature] = (ttest_val.pvalue)
                    else:
                        df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)][iter_feature] = 0

        TablePrinter.printDataFrame(df_new)
        
        result_objects = []
        # Adding the newly created csv
        result_object = ResultObject(df_new, [], DataType.csv,
                              CommandStatus.Success)
        result_object.createName(cname, command_name='sigtest',
                          set_keyword_list=True)
        
        result_objects.append(result_object)
        # create an updated list of column names by removing the common names
        kl1 = df_new.columns
        truncated_kl1, common_name = StatContainer.removeCommonNames(kl1)
        for col in range (0,len(kl1)):
            arr = df_new[kl1[col]]
            result_object = ResultObject(arr, [], DataType.array,
                              CommandStatus.Success)
            command_name = 'sigtest'
            result_object.createName(truncated_kl1[col], command_name=command_name,
                      set_keyword_list=True)

            result_objects.append(result_object)
        return result_objects

    def ArgNotFoundResponse(self, arg_name):
        super().AnalyzeArgNotFoundResponse(arg_name)

    def MultipleArgsFoundResponse(self, arg_name):
        super().AnalyzeMultipleArgsFoundResponse(arg_name)
