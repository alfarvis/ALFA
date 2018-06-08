#!/usr/bin/env python
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
import numpy as np


class StatListColumns(AbstractCommand):
    """
    Compute mean of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify mean command
        """
        return ["list", "columns"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the mean command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.csv)]

    def evaluate(self, array_data):
        """
        List all columns in a csv matrix
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        data = array_data.data
        row_format = "{:>30} {:^15} {:^6} {:<40}"
        if hasattr(data, 'columns'):
            print("Statistics for", " ".join(array_data.keyword_list))
            print(row_format.format("Column_name",
                                    "Column_type", "Size",
                                    "Column_range"))
            for column in data.columns:
                data_column = data[column]
                unique_vals = StatContainer.isCategorical(data_column)
                if unique_vals is not None:
                    column_type = "Categorical"
                elif np.issubdtype(data_column.dtype, np.number):
                    column_type = "Number"
                elif isinstance(data_column[0], str):
                    column_type = "String"
                else:
                    column_type = "Unknown"
                n_unique_vals = str(len(data_column))
                if unique_vals is not None:
                    n_unique_vals = str(len(unique_vals))
                    if len(unique_vals) < 5:
                        column_range = str(unique_vals)
                    else:
                        column_range = ('[' + str(unique_vals[0]) + '...' +
                                        str(unique_vals[-1]) + ']')
                elif np.issubdtype(data_column.dtype, np.number):
                    column_range = "[{:.2f}, {:.2f}]".format(
                        np.min(data_column), np.max(data_column))
                else:
                    column_range = ""
                print(row_format.format(column, column_type, n_unique_vals,
                                        column_range))
            result_object = ResultObject(None, None, None,
                                         CommandStatus.Success)

        return result_object
