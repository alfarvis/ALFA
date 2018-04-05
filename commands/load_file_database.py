#!/usr/bin/env python
"""
Load the file data base into history
"""

import pandas as pd
from collections import namedtuple
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis import package_directory
from .abstract_command import AbstractCommand
from .argument import Argument
import os

FileObject = namedtuple(
    'FileObject', field_names='path, data_type, description')


class LoadDatabase(AbstractCommand):
    """
    Loads a csv file
    """

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["database_load"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        return [Argument(keyword="data_base", optional=False,
                argument_type=DataType.data_base)]

    def checkHeaders(self, headers):
        if headers.size != 4:
            print("Headers in data base file does not match")
            return False
        expected_headers = ['file_name',
                            'file_type', 'keywords', 'description']
        for i, header in enumerate(expected_headers):
            if header != headers[i]:
                print("Header at ", i, " does not match with ", header)
                return False
        return True

    def evaluate(self, data_base):
        """
        Load the file name specified and store it in history
        Parameters:
            data_base has file name which is expected to be of type csv
        """
        command_status = CommandStatus.Error
        result_object = ResultObject(None, None, None, command_status)
        skipped_files = 0
        file_path = os.path.join(package_directory, 'resources',
                                 data_base.data)
        if os.path.isfile(file_path):
            try:
                data_frame = pd.read_csv(file_path)
                self.checkHeaders(data_frame.columns.values)
                result_list = []
                for idx, row in data_frame.iterrows():
                    try:
                        file_type = DataType[row['file_type']]
                    except KeyError:
                        # Depending on verbosity
                        print("file type in line ", idx, " not understood in",
                              row['file_name'])
                        print("Skipping file ...")
                        skipped_files = skipped_files + 1
                        continue
                    file_path = os.path.join(package_directory, 'resources',
                                             row['file_name'])
                    file_object = FileObject(file_path, file_type,
                                             row['description'])
                    keywords = row['keywords'].split(' ')
                    file_res = ResultObject(file_object, keywords,
                                            DataType.file_name)
                    result_list.append(file_res)
                result_object = result_list
            except:
                result_object = ResultObject(None, None, None, command_status)
        return result_object
