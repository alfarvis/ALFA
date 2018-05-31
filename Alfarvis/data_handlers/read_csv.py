#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
import pandas as pd
import re


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
            data, keyword_list, DataType.csv, command_status,
            add_to_cache=True)
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
                col_data, col_keyword_list, DataType.array, command_status,
                add_to_cache=True)
            result_objects.append(result_object)
        return result_objects
