#!/usr/bin/env python
"""
Plot a scatter plot between two arrays
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru


class VizScatter2D(AbstractCommand):
    """
    Plot two arrays against each other in a scatterplot
    """

    def commandTags(self):
        """
        Tags to identify the scatterplot command
        """
        return ["scatterplot","scatter","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the scatter plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array,number=2)]

    def evaluate(self, array_datas):
        """
        Create a scatter plot between two variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)
        
 
        array = df.values
        if StatContainer.ground_truth is None:
            plt.scatter(array[:,0],array[:,1],edgecolor = "None", alpha=0.35)
            #sns.jointplot(x=" ".join(kl1[0]),y=" ".join(kl1[1]),data=array)
        else:
            #sns.jointplot(x=" ".join(kl1[0]),y=" ".join(kl1[1]),data=array,color = StatContainer.ground_truth.data)
            plt.scatter(array[:,0],array[:,1],c = StatContainer.ground_truth.data, cmap = "jet",edgecolor = "None", alpha=0.35)
        plt.xlabel(" ".join(kl1[0]))
        plt.ylabel(" ".join(kl1[1]))
        #plt.legend()
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
