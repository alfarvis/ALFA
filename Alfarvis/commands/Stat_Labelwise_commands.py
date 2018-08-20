#!/usr/bin/env python
"""
Define labelwise mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import numpy as np
import pandas as pd
from .Stat_Container import StatContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru


class Stat_Labelwise_Count(AbstractCommand):
    """
    Compute labelwise count of an array
    """

    def briefDescription(self):
        return "find labelwise count of categories in an array"

    def commandType(self):
        return AbstractCommand.CommandType.Statistics

    def __init__(self, condition=["count"]):
        self._condition = condition

    def commandTags(self):
        """
        return tags that are used to identify labelwise count command
        """
        return (["labelwise " + self._condition[0]] + self._condition +
                ["labelwise", "groupwise"])

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the labelwise count command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1)]

    def performOperation(self, df):
        return df.groupby('ground_truth').count()

    def evaluate(self, array_datas):
        """
        Calculate label-wise mean array store it to history
        Parameters:

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
            array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

        if StatContainer.ground_truth is None:
            gtVals = np.ones(df.shape[0])
        else:
            gtVals = StatContainer.filterGroundTruth()

        # Remove nans:
        df['ground_truth'] = gtVals
        df.dropna(inplace=True)

        gtVals = df['ground_truth']
        uniqVals = StatContainer.isCategorical(gtVals, uniqueCutoff=1000)
        binned_ground_truth = True

        if uniqVals is None and np.issubdtype(gtVals.dtype, np.number):
            # Convert to categorical
            df['ground_truth'] = pd.cut(gtVals, 10)
            binned_ground_truth = True

        # Create groupwise arrays
        result_objects = []

        if uniqVals is not None:
            df_new = self.performOperation(df)

            for col in df_new.columns:
                arr = df_new[col]
                kName = []
                if col == '':
                    kName = array_datas[0].keyword_list
                else:
                    kName.append(cname)
                    kName.append(col)

                result_object = ResultObject(arr, [], DataType.array,
                              CommandStatus.Success)
                command_name = 'labelwise.' + self._condition[0]
                result_object.createName(kName, command_name=command_name,
                          set_keyword_list=True)

                result_objects.append(result_object)
            Printer.Print(df_new)
        else:
            Printer.Print("The array is not of numeric type so cannot",
                          "calculate groupwise " + self._condition[0])
            result_objects.append(result_object)

        return result_objects


class Stat_Labelwise_Mean(Stat_Labelwise_Count):
    def briefDescription(self):
        return "find labelwise mean of categories in an array"

    def __init__(self):
        super(Stat_Labelwise_Mean, self).__init__(["mean", "average"])

    def performOperation(self, df):
        return df.groupby('ground_truth').mean()


class Stat_Labelwise_Stdev(Stat_Labelwise_Count):
    def briefDescription(self):
        return "find labelwise stdev of categories in an array"

    def __init__(self):
        super(Stat_Labelwise_Stdev, self).__init__(["stdev", "standard deviation"])

    def performOperation(self, df):
        return df.groupby('ground_truth').std()


class Stat_Labelwise_Sum(Stat_Labelwise_Count):
    def briefDescription(self):
        return "find labelwise sum of elements in categories"

    def __init__(self):
        super(Stat_Labelwise_Sum, self).__init__(['sum'])

    def performOperation(self, df):
        return df.groupby('ground_truth').sum()
