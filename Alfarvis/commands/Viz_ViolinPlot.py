#!/usr/bin/env python
"""
Plot multiple arrays on a violin plot
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

class Viz_VioloinPlot(AbstractCommand):
    """
    Plot multiple arrays on a violin plot
    """

    def commandTags(self):
        """
        Tags to identify the violin command
        """
        return ["violin","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the violin plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Create a violin plot for multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        
        
        #Code to create the violin plot
        sns.violinplot(data=df)
       
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
