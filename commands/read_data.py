#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 21:55:14 2018

@author: vishwaparekh
"""
import pandas as pd
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject, FileNameObject, ResultObject
from skimage.io import imread


class ReadData:
    @classmethod
    def read(self,file_name):
        self.data_path = file_name.data.path
        self.data_type = file_name.data.data_type
        self.keyword_list = file_name.keyword_list
        self.command_status = CommandStatus.Success
        if self.data_type==DataType.csv:
            return self.read_csv(self)
        elif self.data_type == DataType.image:
            return self.read_image(self)
        elif self.data_type == DataType.algorithm_arg:
            return self.read_algorithm(self)
        elif self.data_type == DataType.trained_model:
            return self.read_trained_model(self)
        elif self.data_type == DataType.imdb:
            return self.read_imdb(self)
        else:
            result_objects = []
            result_objects.append(ResultObject(None,None,None,CommandStatus.Error))
            return result_objects
    
    def read_csv(self):
        data = pd.read_csv(self.data_path)
        result_objects = []
        result_object = ResultObject(data_type=DataType.csv, keyword_list=self.keyword_list, data=data, command_status=self.command_status)
        result_objects.append(result_object)
        cl = data.columns
        for i in range(0,len(data.columns)):
            col_data = data[cl[i]].values
            keyword_list = [cl[i]]
            result_object= ResultObject(data_type=DataType.array, keyword_list=keyword_list, data=col_data, command_status=self.command_status)
            result_objects.append(result_object)
            
        return result_objects
        #Initialize csv command group
        #ML_Analyze(self.data_path)
        
        return result_objects
    
    def read_image(self):
        result_objects = []
        data = imread(self.data_path)
        result_objects.append(ResultObject(data_type=DataType.image, keyword_list=self.keyword_list, data=data, command_status=self.command_status))
        #Initialize image manipulation command group
        return result_objects
    
    #imdb is image database
    def read_imdb(self):
        data = pd.read_csv(self.data_path)
        result_object = ResultObject(data_type=DataType.imdb, keyword_list=self.keyword_list, data=data, command_status=self.command_status)
        #Initialize imdb command group
        return result_object
            

    def read_algorithm(self):
        #load from json/csv
        #function call create_algorithm_from_csv
        a=4

    def read_trained_model(self):
        #load from hpdf5 file type
        # function call load_trained_model
        a=4