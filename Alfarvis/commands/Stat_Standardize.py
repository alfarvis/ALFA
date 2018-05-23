#!/usr/bin/env python2
"""
Define standardize command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy
from sklearn import preprocessing
import copy


class StatMax(AbstractCommand):
    """
    Transform a csv to its standardized values
    """

    def commandTags(self):
        """
        return tags that are used to identify standardize command
        """
        return ["standardize", "scale", "normalize"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the standardize command
        """
        return [Argument(keyword="csv_data", optional=True,
                         argument_type=DataType.csv)]

    def evaluate(self, csv_data):
        """
        Transform a csv to its standardized counterpart

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        keyword_list = csv_data.keyword_list
        keyword_list.extend(["scale", "standardize"])
        data = csv_data.data

        if numpy.issubdtype(data.dtype, numpy.number):
            scaler = preprocessing.StandardScaler().fit(data)
            X_train = scaler.transform(data)
            scaled_data = copy.copy(csv_data.data)
            for i, column in enumerate(csv_data.columns):
                scaled_data[column] = X_train[:, i]

            print("Saving the scaled data...")
            result_object = ResultObject(scaled_data, keyword_list,
                                         DataType.array,
                                         CommandStatus.Success)
        else:
            print("The array is not of numeric type so cannot normalize.",
                  " The data might contain some non-numeric types")

        return result_object
