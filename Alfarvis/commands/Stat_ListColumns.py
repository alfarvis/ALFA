#!/usr/bin/env python
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.history.data_base import Database
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer
import numpy as np


class StatListColumns(AbstractCommand):
    """
    Compute mean of an array
    """

    def __init__(self):
        self.column_type_db = Database()
        self.column_type_db.add(['string', 'str'], 'String')
        self.column_type_db.add(['categorical', 'category'], 'Categorical')
        self.column_type_db.add(['logic', 'logical'], 'Logic')
        self.column_type_db.add(['number', 'numeric'], 'Numeric')
        self.column_type_db.add(['unknown'], 'Unknown')

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
                         argument_type=DataType.csv),
                Argument(keyword="user_conv", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, array_data, user_conv):
        """
        List all columns in a csv matrix
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        data = array_data.data
        req_categories = [res.data for res in
            self.column_type_db.search(user_conv.data)]
        column_strings = {'Categorical': [], 'Numeric': [], 'Logic': [],
                'String': [], 'Unknown': []}
        row_format = "{:>30} {:^15} {:^6} {:<40}"
        if hasattr(data, 'columns'):
            for column in data.columns:
                data_column = data[column]
                data_column.dropna(inplace=True)
                unique_vals = StatContainer.isCategorical(data_column)
                if unique_vals is not None:
                    column_type = "Categorical"
                elif np.issubdtype(data_column.dtype, np.number):
                    column_type = "Numeric"
                elif np.issubdtype(data_column.dtype, np.bool_):
                    column_type = "Logic"
                elif (len(data_column) > 0 and
                      isinstance(data_column.iloc[0], str)):
                    column_type = "String"
                else:
                    column_type = "Unknown"
                # If we did not request specific column just ignore
                if req_categories != [] and column_type not in req_categories:
                    continue
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
                column_strings[column_type].append(
                        row_format.format(column, column_type, n_unique_vals,
                                          column_range))
            Printer.Print("Showing Statistics for",
                          " ".join(array_data.keyword_list))
            print(row_format.format("Column_name", "Column_type", "Size",
                                    "Column_range"))
            for column_type in column_strings:
                if column_strings[column_type] != []:
                    print('\n'.join(column_strings[column_type]))
            result_object = ResultObject(None, None, None,
                                         CommandStatus.Success)

        return result_object
