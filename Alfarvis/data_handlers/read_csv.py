#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
import pandas as pd
import re
import numpy as np


class ReadCSV(AbstractReader):
    # This will split the sentence into multiple keywords using anything except
    # a-z,0-9 and + as a partition
    pattern = re.compile('[^a-zA-Z0-9]+')
    all_caps_pattern = re.compile('^[^a-z]*$')
    col_head_pattern = re.compile('Unnamed: [0-9]+')

    @classmethod
    def data_type(self):
        return DataType.csv

    def read(self, file_path, keyword_list):
        try:
            data = pd.read_csv(file_path)
        except:
            print("File not found")
            return ResultObject(None, None, None, CommandStatus.Error)

        command_status = CommandStatus.Success

        result_objects = []
        result_object = ResultObject(
            data, keyword_list, DataType.csv, command_status)
        result_objects.append(result_object)
        # Too many columns do not extract them individually
        if len(data.columns) > 5000:
            return result_object
        for column in data.columns:
            if self.col_head_pattern.match(column):
                continue
            elif self.all_caps_pattern.match(column):
                col_split = [key_val.lower()
                             for key_val in self.pattern.split(column)]
            else:
                # Add space before upper case
                re.sub(r"([A-Z])", r" \1", column)
                col_split = [key_val.lower()
                             for key_val in self.pattern.split(column)]

            col_data = data[column].values
            col_keyword_list = col_split + keyword_list
            result_object = ResultObject(
                col_data, col_keyword_list, DataType.array, command_status)
            result_objects.append(result_object)
            
            # Checking if a column is categorical and transforming it into
            # a bunch of logical arrays for ease of computation
            uniqVals = np.unique(col_data)
            # Define a percentage cutoff for identifying a variable as a
            # categorical variable
            percCutoff_for_categorical = 0.1 # current cutoff is 10%
            
            if (len(uniqVals)/len(col_data)) <= percCutoff_for_categorical and isinstance(col_data[0],str)==True:
                result_objects = self.add_categories_as_columns(uniqVals,col_data,col_split,keyword_list,result_objects,command_status)
            
        return result_objects

    
    def add_categories_as_columns(self,uniqVals,col_data,col_split,keyword_list,result_objects,command_status):
        """
            Module to convert a categorical column into a bunch of logical
            arrays
        """
        for uniV in uniqVals:                
            categ_data = col_data == uniV
            categ_name = "group class " + str(uniV)
            category_split = [key_val.lower()
                         for key_val in self.pattern.split(categ_name)]
            category_keyword_list = category_split+col_split+keyword_list
            result_object = ResultObject(
            categ_data*1, category_keyword_list, DataType.logical_array, command_status)
            result_objects.append(result_object)
        return result_objects