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
from Alfarvis.Toolboxes.DataGuru import DataGuru


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
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        command_status, df, kl1 = DataGuru.transformArray_to_dataFrame(array_datas)
        if command_status == CommandStatus.Error:
            return ResultObject(None, None, None, CommandStatus.Error)

                
        df.plot()
       
        plt.show(block=False)
            
        result_object = ResultObject(None, None, None,CommandStatus.Success)    

        return result_object
