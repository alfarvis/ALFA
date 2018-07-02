#!/usr/bin/env python
"""
Create a pie plot with multiple categories
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Viz_Container import VizContainer
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



class VizPiePlots(AbstractCommand):
    """
    Plot multiple categories on a single pie plot with error bars
    """

    def commandTags(self):
        """
        Tags to identify the pie plot command
        """
        return ["pie","chart","plot"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the pie plot command
        """
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Create a pie plot 

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        sns.set(color_codes=True)
        stTitle = " ".join(array_data.keyword_list)
        col_data = array_data.data
        uniqVals = np.unique(col_data)
        percCutoff_for_categorical=0.1
        if (len(uniqVals)/len(col_data)) < percCutoff_for_categorical:
            freq_vals = []
            for uniQ in uniqVals:
                ind = (col_data==uniQ)
                freq_vals.append(np.sum(ind*1))
        else: 
            print("Too many unique values to plot on a pie chart\n")
            print("Please select another chart type")

        df = pd.Series(freq_vals, index=uniqVals, name=stTitle)

        f = plt.figure()
        ax = f.add_subplot(111)

        df.plot.pie(figsize=(8, 8), ax=ax)

        plt.show(block=False)
        return VizContainer.createResult(f, array_datas, ['pie'])
