#!/usr/bin/env python
"""
Load the file data base into history
"""

from collections import namedtuple
from pathlib import Path
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus, FileObject
from Alfarvis import package_directory
from Alfarvis.printers import Printer
from .read_folder import ReadFolder
from pathlib import Path
import pandas as pd
import os


class ReadDatabase(AbstractReader):
    """
    Loads a data base that contains locations of other files
    """

    @classmethod
    def data_type(self):
        return DataType.data_base

    def checkHeaders(self, headers):
        if headers.size != 4:
            Printer.Print("Headers in data base file does not match")
            return False
        expected_headers = ['file_name',
                            'file_type', 'keywords', 'description']
        for i, header in enumerate(expected_headers):
            if header != headers[i]:
                Printer.Print("Header at ", i, " does not match with ", header)
                return False
        return True

    def findFilePath(self, file_path):
        mod_file_path = file_path
        if not os.path.isfile(mod_file_path):
            mod_file_path = os.path.join(str(Path.home()),
                                  'AlfaDatabase', file_path)
        if not os.path.isfile(mod_file_path):
            mod_file_path = os.path.join(package_directory, 'resources',
                    file_path)
        if not os.path.isfile(mod_file_path):
            return None
        return mod_file_path

    def read(self, file_path, keyword_list):
        """
        Load the file name specified and store it in history
        Parameters:
            file_path file location which is expected to be of type csv
            keyword_list keywords used to describe the database
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        skipped_files = 0
        mod_file_path = self.findFilePath(file_path)
        if mod_file_path is not None:
            # try:
            data_frame = pd.read_csv(mod_file_path)
            self.checkHeaders(data_frame.columns.values)
            result_list = []
            for idx, row in data_frame.iterrows():
                try:
                    file_type = DataType[row['file_type']]
                except KeyError:
                    # Depending on verbosity
                    Printer.Print("file type in line ", idx, " not understood in",
                          row['file_name'])
                    Printer.Print("Skipping file ...")
                    skipped_files = skipped_files + 1
                    continue
                if file_type == DataType.folder:
                    Printer.Print("Loading folder: ", row['file_name'])
                    read_folder = ReadFolder()
                    result = read_folder.read(
                            row['file_name'], row['keywords'].split(),
                            'recursive' == row['description'])
                    if result.command_status == CommandStatus.Success:
                        result_list.append(result)
                    else:
                        Printer.Print("Failed to load folder: ", row['file_name'])
                    continue
                row_file_path = self.findFilePath(row['file_name'])
                if row_file_path is None:
                    Printer.Print("Cannot find file: ", row['file_name'])
                    continue
                file_object = FileObject(row_file_path, file_type,
                                         row['description'], False)
                keywords = row['keywords'].split(' ')
                file_res = ResultObject(file_object, keywords,
                                        DataType.file_name)
                file_res.createName(keywords)
                result_list.append(file_res)
            result_object = result_list
            # except:
            #    result_object = ResultObject(None, None, None, CommandStatus.Error)
        return result_object
