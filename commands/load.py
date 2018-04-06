#!/usr/bin/env python2
"""
Define load command
"""
import pandas as pd
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject, ResultObject
from Alfarvis.commands.read_data import ReadData
from .abstract_command import AbstractCommand
from .argument import Argument

import os


class Load(AbstractCommand):
    """
    Loads a csv file
    """

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["load", "import"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for executing
        the load command
        """
        return [Argument(keyword="file_name", optional=False, argument_type=DataType.file_name)]

    def evaluate(self, file_name):
        """
        Load the file name specified and store it in history
        Parameters:
            file_name has two entries
                1. Path of the file to load
                2. Type of the file to load
        """
        command_status = CommandStatus.Error
        result_object = ResultObject(None ,None , None,command_status)
        
        if os.path.isfile(file_name.data.path):
            try:                
                result_object = ReadData.read(file_name)                                
            except:                
                result_object = ResultObject(None ,None , None, command_status)
        
        return result_object
