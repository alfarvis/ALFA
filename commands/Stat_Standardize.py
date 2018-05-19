#!/usr/bin/env python2
"""
Define mean command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
#from Alfarvis.commands.read_data import ReadData
from Alfarvis.data_handlers import create_reader_dictionary
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore
import numpy
import re
from sklearn import preprocessing


class StatMax(AbstractCommand):
    """
    Transform a csv to its standardized values
    """

    def __init__(self):
        self.reader_dictionary = create_reader_dictionary()

    def commandTags(self):
        """
        return tags that are used to identify standardize command
        """
        return ["standardize","scale","normalize"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the standardize command
        """
        return [Argument(keyword="csv_data", optional=True, 
                         argument_type=DataType.csv)]

    def evaluate(self, csv_data=None):
        """
        Transform a csv to its standardized counterpart
            
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if csv_data is not None:
            keyword_list = csv_data.keyword_list
            VarStore.SetCurrentCSV(csv_data.data," ".join(keyword_list))                    
        else:
            #This will split the sentence into multiple keywords using anything except
            #a-z,0-9 and + as a partition
            pattern = re.compile('[^a-z0-9]+')
            keyword_list = pattern.split(VarStore.currCSV_name)    
            
        
        scaler = preprocessing.StandardScaler().fit(VarStore.X)
        X_train = scaler.transform(VarStore.X)
        data1 = csv_data.data
        for i in range (len(VarStore.columnList)):
            data1[VarStore.columnList[i]] = X_train[:,i]
    
        
        print("Saving the scaled data...")
        result_object = ResultObject(data1, keyword_list, DataType.array, CommandStatus.Success)
            

        return result_object
