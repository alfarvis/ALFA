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


class StatSigTest(AbstractCommand):
    """
    Calculates ttest for a predictor variable
    """

    def commandTags(self):
        """
        return tags that are used to identify ttest command
        """
        return ["ttest", "p", "value"]

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
        #                                  DataType.array, CommandStatus.Success)
