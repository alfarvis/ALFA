#!/usr/bin/env python3
"""
Set ground truth
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore
import numpy
import re

import os


class SetGT(AbstractCommand):
    """
    Sets the ground truth for data guru operations
    """

    def commandTags(self):
        """
        return tags that are used to identify set ground truth command
        """
        return ["setgt","set", "ground","truth"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the set ground truth command
        """
        return [Argument(keyword="array_data", optional=False, 
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate average value of the array and store it to history
        Parameters:
            
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        
        keyword_list = array_data.keyword_list
        VarStore.SetGroundTruth(array_data.data," ".join(keyword_list))
        print("Ground truth for data mining has been set to ", " ".join(keyword_list))
        result_object = ResultObject(None, None, None, CommandStatus.Success)
            

        return result_object