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
from Alfarvis.Toolboxes.DataGuru import DataGuru

class VizHistogram(AbstractCommand):
    """
    Plot multiple array histograms on a single plot
    """

    def commandTags(self):
        """
        Tags to identify the histogram command
        """
        return ["histogram","hist","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the histogram command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Create a histogram for multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas,1)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        
        
        #TODO Create an argument for setting number of bins
        if df.shape[1]==1:
            if StatContainer.isCategorical(df[df.columns[0]]) is not None:
                sns.countplot(x=kl1[0],data = df)
            else:
                df.plot.hist(stacked=True, bins=20)        
        else:                
            df.plot.hist(stacked=True, bins=20)
       
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
