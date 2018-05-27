#!/usr/bin/env python
"""
Plot multiple arrays in a single line plot
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class VizPlotLine(AbstractCommand):
    """
    Plot multiple arrays in a single line plot
    """

    def commandTags(self):
        """
        Tags to identify the lineplot command
        """
        return ["lineplot", "line","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the lineplot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Create a line plot 

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        
        #Create a combined array and keyword list
        kl1 =[]
        arrays = []
        array_size = 0
        sns.set(color_codes=True)
        for array_data in array_datas:
            kl1 = kl1+array_data.keyword_list
            arrays.append(array_data.data)
            if array_size == 0:
                array_size = array_data.data.size
            else:
                if array_size != array_data.data.size:
                    print("The arrays to be plotted are not of the same dimensions")
                    result_object = ResultObject(None, None, None, CommandStatus.Error)
                    return result_object
            if (np.issubdtype(array_data.data.dtype, np.number))==False:  
                print("Please provide numeric arrays")
                result_object = ResultObject(None, None, None, CommandStatus.Error)
                return result_object
            plt.plot(array_data.data,label = " ".join(array_data.keyword_list))
                
        kl2 = set(kl1)
        keyword_list = list(kl2)
        array = np.array(arrays)
        
        #plt.plot(np.transpose(array))
        #Plot the legend to the right of the box
        plt.legend()
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
