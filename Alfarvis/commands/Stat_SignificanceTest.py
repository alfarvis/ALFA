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
import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class StatSigTest(AbstractCommand):
    """
    Calculates ttest for a predictor variable
    """

    def commandTags(self):
        """
        return tags that are used to identify ttest command
        """
        return ["ttest", "p", "value", "t test"]

    def argumentTypes(self):
        """
        A list of  argument objects that specify the inputs needed for
        executing the ttest command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data=None):
        """
        Calculate ttest of the array and store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        arr = array_data.data
        if np.issubdtype(arr.dtype, np.number):
            if StatContainer.ground_truth is not None:
                gt1 = (StatContainer.ground_truth.data)
                uniqVals = np.unique(gt1)
                pVals = []
                startFlag = 1
                # TODO: Remove nans from arrays!!
                # TODO COmplete this: Idea is to create a heatmap like the one
                # we did for correlation
                for uniV in uniqVals:

                    stTitle = " ".join(["group ", str(uniV)])
                    a = arr[gt1 == uniV]
                    allp = []
                    for iter in range(len(uniqVals)):
                        b = arr[gt1 == uniqVals[iter]]
                        if uniV == uniqVals[iter]:
                            allp.append(0)
                        else:
                            ttest_val = scipy.stats.ttest_ind(a, b, axis=0, equal_var=False)
                            allp.append(ttest_val.pvalue)
                    if startFlag == 1:
                        pVals = pd.DataFrame({stTitle: allp})
                        startFlag = 0
                    else:
                        pVals[stTitle] = allp
            else:
                print("Please set ground truth before running this command")
                return result_object
        else:
            print("Please provide numerical array for ttest")
            return result_object

        print("Displaying the result as a heatmap")
        sns.heatmap(pVals, cbar=True, square=True, annot=True, fmt='.2f', annot_kws={'size': 15},
           xticklabels=pVals.columns, yticklabels=pVals.columns,
           cmap='jet')
        plt.show(block=False)
        result_object = ResultObject(None, None, None, CommandStatus.Success)
        return result_object
        # Debug this @Vishwa
        # keyword_list = array_data.keyword_list
        # array = array_data.data
        # ground_truth = StatContainer.ground_truth
        # if ground_truth is not None:
        #     # TODO: THis will only run if the ground truth has only two labels
        #     a = array[ground_truth.data == 1]
        #     b = array[ground_truth.data == 2]
        #     ttest_val = scipy.stats.ttest_ind(a, b, axis=0, equal_var=False)
        #     print("p value for prediction of ",
        #           " ".join(ground_truth.keyword_list),
        #           "using ", " ".join(keyword_list), " is ", ttest_val.pvalue)
        #     result_object = ResultObject(ttest_val.pvalue, keyword_list,
        # DataType.array, CommandStatus.Success)
