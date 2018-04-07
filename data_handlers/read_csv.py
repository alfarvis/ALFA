#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
import pandas as pd

class ReadCSV(AbstractReader):
    @classmethod
    def data_type(self):
        return DataType.csv
        
    def read(self, file_path, keyword_list):
        try:
            data = pd.read_csv(file_path)
            command_status = CommandStatus.Success
        except:
            return ResultObject(None, None, None, CommandStatus.Error)
        result_objects = []
        result_object = ResultObject(data, keyword_list, DataType.csv, command_status)
        result_objects.append(result_object)
        # Too many columns do not extract them individually
        if len(data.columns) > 20:
            return result_object
        for column in data.columns:
            col_data = data[column].values
            # TODO process column to remove capitals, special characters and split the text
            keyword_list = [column]
            result_object = ResultObject(col_data, keyword_list, DataType.array, command_status)
            result_objects.append(result_object)

        return result_objects
