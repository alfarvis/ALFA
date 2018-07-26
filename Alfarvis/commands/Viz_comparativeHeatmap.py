#!/usr/bin/env python
"""
Create a heatmap for visualization of the data
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
from .Viz_Container import VizContainer
from Alfarvis.Toolboxes.DataGuru import DataGuru
import pandas as pd


class Stat_RelationMap(AbstractCommand):
    """
    create a heatmap for visualizing relationship between two variables
    """

    def commandTags(self):
        """
        Tags to identify the relationship visualization
        """
        return ["visualize relationship"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the heatmap command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=2)]

    def evaluate(self, array_datas):
        """
        Visualize the relationship between variables

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)

        sns.set(color_codes=True)
        
        isCategorical = True
        count=0
        df = pd.DataFrame()
        for array_data in array_datas:
            if (np.issubdtype(array_data.data.dtype, np.number)) == True:
                isCategorical = False
            if count==0:
                
                df[" ".join(array_data.keyword_list)] = array_data.data
                count = 1
                #df.index = arr
            else:
                df[" ".join(array_data.keyword_list)] = array_data.data
        
        if isCategorical == True:
            df.dropna(inplace=True)   
            df = df.pivot_table(index=df.columns[0],columns=df.columns[1],aggfunc=np.size,fill_value=0)
        
            print("Displaying heatmap")
            f = plt.figure()
            sns.heatmap(df)

            plt.show(block=False)
            return VizContainer.createResult(f, array_datas, ['heatmap'])
        else:
            print("The data to plot is not categorical, Please use scatter plot")
            return result_object
