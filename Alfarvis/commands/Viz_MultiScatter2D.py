#!/usr/bin/env python
"""
Plot multiple arrays in a multidimensional scatterplot
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


class VizMultiScatter2D(AbstractCommand):
    """
    Plot multiple arrays against each other in a multidimensional scatterplot
    """

    def commandTags(self):
        """
        Tags to identify the multidimensional scatterplot command
        """
        return ["multiscatterplot","multi","multiple","scatter","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the multiscatter command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=-1)]

    def evaluate(self, array_datas):
        """
        Create a scatter plot between multiple variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        
        
        if StatContainer.ground_truth is None:
            pd.scatter_matrix(df, alpha=0.2, diagonal='kde')
            #sns.jointplot(x=" ".join(kl1[0]),y=" ".join(kl1[1]),data=array)
        else:
            #sns.jointplot(x=" ".join(kl1[0]),y=" ".join(kl1[1]),data=array,color = StatContainer.ground_truth.data)
            pd.scatter_matrix(df, alpha=0.2, diagonal='kde',c = StatContainer.ground_truth.data,cmap = "jet")
        #plt.xlabel(" ".join(kl1[0]))
        #plt.ylabel(" ".join(kl1[1]))
        #plt.legend()
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
