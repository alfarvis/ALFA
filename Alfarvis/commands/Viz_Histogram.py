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


class VizHistogram(AbstractCommand):
    """
    Plot multiple array histograms on a single plot
    """

    def commandTags(self):
        """
        Tags to identify the scatterplot command
        """
        return ["histogram","hist","plot"]

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
            kl1.append(array_data.keyword_list)
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
                    
        
        
        
        #TODO Create an argument for setting number of bins
        df.plot.hist(stacked=True, bins=20)
       
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
