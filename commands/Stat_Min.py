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

import os


class StatMin(AbstractCommand):
    """
    Calculate min of an array
    """

    def __init__(self):
        self.reader_dictionary = create_reader_dictionary()

    def commandTags(self):
        """
        return tags that are used to identify min command
        """
        return ["min","minimum","lowest"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the min command
        """
        return [Argument(keyword="array_data", optional=True, 
                         argument_type=DataType.array)]

    def evaluate(self, array_data=None):
        """
        Calculate min value of the array and store it to history
        Parameters:
            
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if array_data is not None:
            keyword_list = array_data.keyword_list
            VarStore.SetCurrentArray(array_data.data," ".join(keyword_list))                    
        else:
            #This will split the sentence into multiple keywords using anything except
            #a-z,0-9 and + as a partition
            pattern = re.compile('[^a-z0-9]+')
            keyword_list = pattern.split(VarStore.currArray_name)    
            
        
        min_val = numpy.min(VarStore.currArray)
    
        
        print("Minimum of ", " ".join(keyword_list), " is ", min_val)
        result_object = ResultObject(min_val, keyword_list, DataType.array, CommandStatus.Success)
            

        return result_object
