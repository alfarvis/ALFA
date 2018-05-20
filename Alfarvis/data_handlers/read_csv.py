#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore
import pandas as pd
import re

class ReadCSV(AbstractReader):
    pattern = re.compile('[^a-z0-9]+')
    col_head_pattern = re.compile('Unnamed: [0-9]+')

    @classmethod
    def data_type(self):
        return DataType.csv
        
    def read(self, file_path, keyword_list):
        try:
            data = pd.read_csv(file_path)
            VarStore.SetCurrentCSV(data,keyword_list[0])
            command_status = CommandStatus.Success
        except:
            return ResultObject(None, None, None, CommandStatus.Error)
        result_objects = []
        result_object = ResultObject(data, keyword_list, DataType.csv, command_status)
        result_objects.append(result_object)
        # Too many columns do not extract them individually
        if len(data.columns) > 50:
            return result_object
        for column in data.columns:
            if self.col_head_pattern.match(column):
                continue
            col_data = data[column].values
            # TODO process column to remove capitals, special characters and split the text
            col_keyword_list = self.pattern.split(column) + keyword_list
            result_object = ResultObject(col_data, col_keyword_list, DataType.array, command_status)
            result_objects.append(result_object)

        return result_objects
