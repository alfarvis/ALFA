#!/usr/bin/env python
"""
Plot multiple arrays on a histogram
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
        executing the histoogram command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Create a scatter plot between multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        
        #Create a combined array and keyword list
        kl1 =[]
        arrays = []
        array_size = 0
        sns.set(color_codes=True)
        for array_data in array_datas:
            kl1.append(" ".join(array_data.keyword_list))
            arrays.append(array_data.data)
            if array_size == 0:
                array_size = array_data.data.size
                df = pd.DataFrame({(" ".join(array_data.keyword_list)):array_data.data})
            else:
                if array_size != array_data.data.size:
                    print("The arrays to be plotted are not of the same dimensions")
                    result_object = ResultObject(None, None, None, CommandStatus.Error)
                    return result_object
                df[(" ".join(array_data.keyword_list))] = pd.Series(array_data.data)
            if (np.issubdtype(array_data.data.dtype, np.number))==False:  
                print("Please provide numeric arrays")
                result_object = ResultObject(None, None, None, CommandStatus.Error)
                return result_object
                    
        
        
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
