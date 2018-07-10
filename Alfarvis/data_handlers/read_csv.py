#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import (DataType, ResultObject, CommandStatus,
                                        DataObject, splitPattern)
from Alfarvis.commands.Stat_ListColumns import StatListColumns
from Alfarvis.commands.Stat_Container import StatContainer
import pandas as pd
import re


class ReadCSV(AbstractReader):
    list_command = StatListColumns()
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
        result_object.createName(keyword_list)
        result_objects.append(result_object)
        # Too many columns do not extract them individually
        if len(data.columns) > 5000:
            return result_object
        num_unique = float("inf")
        current_gt = None
        for column in data.columns:
            if self.col_head_pattern.match(column):
                continue
            else:
                col_split = splitPattern(column)
            col_data = data[column].values
            col_keyword_list = col_split + keyword_list
            result_object = ResultObject(
                col_data, col_keyword_list, DataType.array, command_status,
                add_to_cache=True)
            result_object.createName(col_keyword_list)
            result_objects.append(result_object)

            unique_vals = StatContainer.isCategorical(col_data)

            if unique_vals is not None:
                if len(unique_vals) < num_unique:
                    current_gt = DataObject(col_data, col_keyword_list)
                    num_unique = len(unique_vals)
                result_objects = self.add_categories_as_columns(
                    unique_vals, col_data, col_split, keyword_list,
                    result_objects, command_status)
        # List the information about csv
        print("Loaded " + " ".join(keyword_list))
        if current_gt is not None:
            StatContainer.ground_truth = current_gt
            print("Setting ground truth to ", " ".join(current_gt.keyword_list))
        self.list_command.evaluate(result_objects[0])
        return result_objects

    def add_categories_as_columns(self, uniqVals, col_data, col_split,
                                  keyword_list, result_objects,
                                  command_status):
        """
            Module to convert a categorical column into a bunch of logical
            arrays
        """
        for uniV in uniqVals:
            categ_data = col_data == uniV
            categ_name = "group class " + str(uniV)
            category_split = [key_val.lower()
                              for key_val in splitPattern(categ_name)]
            category_keyword_list = category_split + col_split + keyword_list
            result_object = ResultObject(
                categ_data * 1, category_keyword_list,
                DataType.logical_array, command_status)
            result_object.createName(category_keyword_list)
            result_objects.append(result_object)
        return result_objects
