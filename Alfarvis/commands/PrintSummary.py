#!/usr/bin/env python
"""
Print summary of a dataframe
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer, TablePrinter
import numpy as np
import pandas as pd
from .Stat_Container import StatContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru
import scipy


class DataSummary(AbstractCommand):
    """
    Print summary
    """

    def briefDescription(self):
        return "print summary statistics of a dataframe"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def commandName(self):
        return "statistics.summary"

    def __init__(self, condition=["summary","summarize"]):
        self._condition = condition

    def commandTags(self):
        """
        return tags that are used to identify print summary command
        """
        return (self._condition)

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the print summary command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1, fill_from_cache=False), 
                Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1, fill_from_cache=False)]

    def performOperation(self, df):
        df_new = pd.DataFrame()
        df_new['features'] = df.columns
        df_new['mean'] = df.mean().values
        df_new['stdev'] = df.std().values
        df_new['min'] = df.min().values
        df_new['max'] = df.max().values

        return df_new

    def evaluate(self, array_datas,data_frame):
        """
        Calculate label-wise mean array store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Success)
        
        if data_frame is not None:
            df = data_frame.data
            cname = data_frame.name
        elif array_datas is not None:
            command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas)
            if len(cname)==0:
                cname = ".".join(kl1)
            if command_status == CommandStatus.Error:
                return ResultObject(None, None, None, CommandStatus.Error)
        else: 
            Printer.Print("Please provide data frame or arrays to analyze")
            return ResultObject(None, None, None, CommandStatus.Error)

        df_new = self.performOperation(df)
        TablePrinter.printDataFrame(df_new)
        
        result_objects = []
        # Adding the newly created CSV
        result_object = ResultObject(df_new, [], DataType.csv,
                              CommandStatus.Success)
        command_name = "smry"
        result_object.createName(cname, command_name=command_name,
                          set_keyword_list=True)
        
        result_objects.append(result_object)
        # create an updated list of column names by removing the common names
        kl1 = df_new.columns
        truncated_kl1, common_name = StatContainer.removeCommonNames(kl1)
        for col in range (0,len(kl1)):
            arr = df_new[kl1[col]]
            result_object = ResultObject(arr, [], DataType.array,
                              CommandStatus.Success)
            
            result_object.createName(truncated_kl1[col], command_name=command_name,
                      set_keyword_list=True)

            result_objects.append(result_object)
            
        return result_objects
        

    def ArgNotFoundResponse(self, arg_name):
        Printer.Print("Which data frame do you want me to summarize?")

    def ArgFoundResponse(self, arg_name):
        Printer.Print("Found the data frame")

    def MultipleArgsFoundResponse(self, arg_name):
        super().MultipleArgsFoundResponse(file_name, 'data frames', 0)


class DataGroupSummary(DataSummary):

    def __init__(self):
        super(DataGroupSummary, self).__init__(["groupwise", "labelwise", "summary","label wise", "group wise"])

    def briefDescription(self):
        return "print label wise summary"

    def commandName(self):
        return "statistics.groupwiseSummary"

    def performOperation(self, df):
        if StatContainer.ground_truth is None or len(StatContainer.ground_truth.data) != df.shape[0]:
            gtVals = np.ones(df.shape[0])
            gtName = 'ground_truth'
        else:
            gtVals = StatContainer.filterGroundTruth()
            gtName = StatContainer.ground_truth.name
        df[gtName] = gtVals
        uniqVals = StatContainer.isCategorical(gtVals)
        df_new = pd.DataFrame()
        if uniqVals is not None:
            if gtName in df.columns:
                df_new['features'] = df.columns.drop(gtName).values
            else:
                df_new['features'] = df.columns
            gb = df.groupby(gtName)
            gb_mean = gb.mean().transpose()
            gb_std = gb.std().transpose()
            for iter in range(len(uniqVals)):
                df_new[str(uniqVals[iter]) + '_mean'] = gb_mean.values[:, iter]
                df_new[str(uniqVals[iter]) + '_stdev'] = gb_std.values[:, iter]
            for iter in range(len(uniqVals)):
                for iter1 in range(iter + 1, len(uniqVals)):
                    df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)] = np.zeros(df_new.shape[0])
            allCols = df_new['features']
            for iter_feature in range(len(df_new['features'])):
                arr = df[allCols[iter_feature]]
                for iter in range(len(uniqVals)):
                    uniV = uniqVals[iter]
                    a = arr[gtVals == uniV]
                    for iter1 in range(iter + 1, len(uniqVals)):
                        b = arr[gtVals == uniqVals[iter1]]
                        if uniV != uniqVals[iter1]:
                            ttest_val = scipy.stats.ttest_ind(a, b, axis=0, equal_var=False)
                            df_new.at[iter_feature, 'pValue: ' + str(iter) + ' vs ' + str(iter1)] = (ttest_val.pvalue)
        return df_new
