#!/usr/bin/env python
"""
Define labelwise sum command
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

class Stat_Labelwise_Sum(AbstractCommand):
    """
    Compute labelwise sum of an array
    """

    def commandTags(self):
        """
        return tags that are used to identify mean command
        """
        return ["labelwise sum", "labelwise", "groupwise sum", "groupwise", "sum"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the labelwise sum command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Calculate label-wise sum array store it to history
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
        uniqVals = StatContainer.isCategorical(gtVals)
        
        #Create groupwise arrays
        result_objects = []
        
        if uniqVals is not None:
            df_new = df.groupby('ground_truth').sum()
            
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
                result_object.createName(kName, command_name='labelwise sum',
                          set_keyword_list=True)
            
                result_objects.append(result_object)
            Printer.Print(df_new)
        else:
            Printer.Print("The array is not of numeric type so cannot",
                          "calculate groupwise sum")
            result_objects.append(result_object)
            
        return result_objects
