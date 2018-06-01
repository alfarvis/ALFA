#!/usr/bin/env python
"""
Create a bar plot with multiple variables
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
import pandas as pd
from Alfarvis.Toolboxes.DataGuru import DataGuru


class VizBarPlots(AbstractCommand):
    """
    Plot multiple features on a single bar plot with error bars
    """

    def commandTags(self):
        """
        Tags to identify the bar plot command
        """
        return ["bar","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the bar plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Create a bar plot between multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        
        
        if StatContainer.ground_truth is None:
            print("Please set a feature vector to ground truth by typing set ground truth before using this command")
            result_object = ResultObject(None, None, None, CommandStatus.Error)
            return result_object
        else:
            gtVals = StatContainer.ground_truth.data
            
            uniqVals = np.unique(gtVals)
            rFlag = 0
            for uniV in uniqVals:                
                ind = gtVals == uniV
                array_vals = df.values
                if rFlag==0:
                    df_mean = pd.DataFrame({'group '+str(uniV):np.mean(array_vals[ind,:],0)})
                    df_errors = pd.DataFrame({'group '+str(uniV):np.std(array_vals[ind,:],0)})
                    rFlag=rFlag+1
                else:
                    df_mean['group '+str(uniV)] = np.mean(array_vals[ind,:],0)
                    df_errors['group '+str(uniV)]=np.std(array_vals[ind,:],0)
            
        df_mean.index=(kl1)
        df_errors.index = kl1
        df_mean.plot.bar(yerr=df_errors,cmap="jet")
       
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
