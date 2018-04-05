#!/usr/bin/env python2
"""
Define load command
"""
import pandas as pd
from Alfarvis.basic_definitions import (DataType, CommandStatus, DataObject,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from skimage.io import imread
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
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        return [Argument(keyword="file_name", optional=False,
                         argument_type=DataType.file_name)]

    def evaluate(self, file_name):
        """
        Load the file name specified and store it in history
        Parameters:
            file_name has two entries
                1. Path of the file to load
                2. Type of the file to load
        """
        command_status = CommandStatus.Error
        result_object = ResultObject(None,None ,None , command_status)
        
        if os.path.isfile(file_name.data.path):
            try:
                data_path = file_name.data.path
                data_type = file_name.data.data_type
                if data_type==DataType.csv:
                    data = pd.read_csv(data_path)
                elif data_type == DataType.image:
                    data = imread(data_path)
                elif data_type == DataType.algorithm_arg:
                    #load from json/csv
                    #function call create_algorithm_from_csv
                    a=4
                elif data_type == DataType.trained_model:
                    #load from hpdf5 file type
                    # function call load_trained_model
                    a=4
                elif data_type == DataType.imdb:
                    data = pd.read_csv(data_path)
                # TODO: Add for imdb
                    
                
                
                command_status = CommandStatus.Success
                keyword_list = file_name.keyword_list
                csv_object = DataObject(data, keyword_list)
                
                result_object = ResultObject(csv_object, keyword_list,
                                             data_type, command_status)
                print("Loaded file: ", os.path.basename(file_name.data.path))
                
                
            except:                
                result_object = ResultObject(None,None ,None , command_status)
        
        return result_object
