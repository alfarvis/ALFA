#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import (DataType, ResultObject, CommandStatus,
                                        DataObject, splitPattern)
from Alfarvis.commands.Stat_ListColumns import StatListColumns
from Alfarvis.commands.Stat_Container import StatContainer
from Alfarvis.printers import Printer
import pandas as pd
import re


class ReadCSV(AbstractReader):
    list_command = StatListColumns()
    col_head_pattern = re.compile('Unnamed: [0-9]+')
    currency_dict = {ord('$'): None, ord(','): None}

    @property
    def read_in_background(self):
        return True

    @classmethod
    def data_type(self):
        return DataType.csv

    def preRead(self, file_path, keyword_list):
        command_status = CommandStatus.Success
        try:
            data = pd.read_csv(file_path)
        except:
            try:
                data = pd.read_excel(file_path)
            except:
                return ResultObject("File not found", None, None, CommandStatus.Error)
        result_objects = []
        result_object = ResultObject(
            data, keyword_list, DataType.csv, command_status,
            add_to_cache=True)
        result_object.createName(result_object.keyword_list)
        result_objects.append(result_object)
        # Too many columns do not extract them individually
        if len(data.columns) > 5000:
            return result_objects
        new_column_names = []
        # num_unique = float("inf")  # Used for smallest unique vec finding
        #current_gt = None
        for column in data.columns:
            if self.col_head_pattern.match(column):
                data.drop(column, axis=1, inplace=True)
                continue
            else:
                col_split = splitPattern(column)
            col_data = data[column].values
            col_keyword_list = col_split

            N = col_data.size
            if N == 0:
                continue
            if isinstance(col_data[0], str):
                if '%' in col_data[0]:
                    try:
                        col_data = data[column].str.rstrip('%').astype(float,
                                       copy=False)
                        data[column] = col_data
                        if 'percent' not in col_keyword_list:
                            col_keyword_list.append('percent')
                    except ValueError:
                        pass
                elif '$' in col_data[0] or ',' in col_data[0]:
                    try:
                        col_data = data[
                                column].str.translate(
                                self.currency_dict).astype(float, copy=False)
                        data[column] = col_data
                        if '$' not in col_keyword_list:
                            col_keyword_list.append('$')
                    except ValueError:
                        pass
            result_object = ResultObject(
                col_data, col_keyword_list, DataType.array, command_status,
                add_to_cache=True)
            result_object.createName(col_keyword_list)
            new_column_names.append(result_object.name)
            result_objects.append(result_object)
            # For now removing unique value search which is pretty slow
            #unique_vals = StatContainer.isCategorical(col_data)
            # if unique_vals is not None:
            #    if len(unique_vals) < num_unique:
            #        current_gt = result_object
            #        num_unique = len(unique_vals)
            #    # Do not add unique values as columns unless they are only a
            #    # few
            #    # if len(unique_vals) < 5:
            #    #    result_objects = self.add_categories_as_columns(
            #    #    unique_vals, col_data, col_split,
            #    #    result_objects, command_status)
        # Replace columns:
        data.columns = new_column_names
        # if current_gt is not None:
        #    StatContainer.ground_truth = current_gt
        return result_objects

    def read(self, file_path, keyword_list, pre_evaluate_results):
        if type(pre_evaluate_results) != list:
            Printer.Print("No preevaluation done!",
                          " Please file a bug report with the chat")
            return ResultObject(None, None, None, CommandStatus.Error)
        # List the information about csv
        Printer.Print("Loaded " + " ".join(keyword_list))
        self.list_command.evaluate(pre_evaluate_results[0], DataObject([''], []))
        return pre_evaluate_results

    def add_categories_as_columns(self, uniqVals, col_data, col_split,
                                  result_objects,
                                  command_status):
        """
            Module to convert a categorical column into a bunch of logical
            arrays
        """
        for uniV in uniqVals:
            categ_data = col_data == uniV
            categ_name = str(uniV)
            category_split = [key_val.lower()
                              for key_val in splitPattern(categ_name)]
            category_keyword_list = category_split + col_split
            result_object = ResultObject(
                categ_data * 1, category_keyword_list,
                DataType.logical_array, command_status)
            result_object.createName(category_keyword_list)
            result_objects.append(result_object)
        return result_objects
