#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
import pandas as pd
import re


class ReadCSV(AbstractReader):
    # This will split the sentence into multiple keywords using anything except
    # a-z,0-9 and + as a partition
    pattern = re.compile('[^a-z0-9]+')
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
            col_data = data[column].values
            # TODO process column to remove capitals, special characters
            # and split the text
            col_keyword_list = self.pattern.split(column) + keyword_list
            result_object = ResultObject(
                col_data, col_keyword_list, DataType.array, command_status)
            result_objects.append(result_object)
        return result_objects
