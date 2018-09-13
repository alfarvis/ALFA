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

    def __init__(self, condition=["summary"]):
        self._condition = condition

    def commandTags(self):
        """
        return tags that are used to identify print summary command
        """
        return (["print"] + self._condition)

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the print summary command
        """
        return [Argument(keyword="data_frame", optional=False,
                         argument_type=DataType.csv, number=1)]

    def performOperation(self, df):
        df_new = pd.DataFrame()
        df_new['features'] = df.columns
        df_new['mean'] = df.mean().values
        df_new['stdev'] = df.std().values
        df_new['min'] = df.min().values
        df_new['max'] = df.max().values

        return df_new

    def evaluate(self, data_frame):
        """
        Calculate label-wise mean array store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Success)

        df_new = self.performOperation(data_frame.data)
        TablePrinter.printDataFrame(df_new)

        return result_object


class DataGroupSummary(DataSummary):

    def __init__(self):
        super(DataGroupSummary, self).__init__(["groupwise", "labelwise", "summary", "label wise", "group wise"])

    def briefDescription(self):
        return "print label wise summary"

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
                for iter1 in range(len(uniqVals)):
                    df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)] = np.zeros(df_new.shape[0])
            allCols = df_new['features']
            for iter_feature in range(len(df_new['features'])):
                arr = df[allCols[iter_feature]]
                for iter in range(len(uniqVals)):
                    uniV = uniqVals[iter]
                    a = arr[gtVals == uniV]
                    for iter1 in range(len(uniqVals)):
                        b = arr[gtVals == uniqVals[iter1]]
                        if uniV != uniqVals[iter1]:
                            ttest_val = scipy.stats.ttest_ind(a, b, axis=0, equal_var=False)
                            df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)][iter_feature] = (ttest_val.pvalue)
                        else:
                            df_new['pValue: ' + str(iter) + ' vs ' + str(iter1)][iter_feature] = 0
        return df_new