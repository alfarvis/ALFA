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
from Alfarvis.Toolboxes.DataGuru import DataGuru


class Stat_Standardize(AbstractCommand):
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
        data = csv_data.data

        # if numpy.issubdtype(data.dtype, numpy.number):
        for column in data.columns:
            col_data = data[column]
            uniqVals = numpy.unique(col_data)
            percCutoff_for_categorical = 0.1
            if (len(uniqVals) / len(col_data)) > percCutoff_for_categorical and isinstance(col_data[0], str) == False:
                col_data = (col_data - numpy.mean(col_data)) / numpy.std(col_data)
            data[column] = col_data

        print("Saving the scaled data...")
        result_object = ResultObject(data, [],
                                     DataType.csv,
                                     CommandStatus.Success)
        result_object.createName(csv_data.keyword_list,
                                 command_name=self.commandTags()[0],
                                 set_keyword_list=True)

        return result_object
