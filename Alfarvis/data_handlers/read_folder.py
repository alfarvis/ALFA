#!/usr/bin/env python
"""
Load the file data base into history
"""

from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus, FileObject, splitPattern, createName
from Alfarvis.printers import Printer
from Alfarvis.history.type_data_base import TypeDatabase
import os


class FolderObject:
    def __init__(self, file_name_database, folder_path):
        self.file_name_database = file_name_database
        self.folder_path = folder_path


class ReadFolder(AbstractReader):
    """
    Loads a data base that contains locations of other files
    """
    @classmethod
    def data_type(self):
        return DataType.folder

    def checkEndsWith(self, string, pattern_list):
        for pattern in pattern_list:
            if string.endswith(pattern):
                return True
        return False

    def addFile(self, dir_entry, file_type, folder_database, parent_path):
        base_name = os.path.basename(dir_entry.name)
        keywords = splitPattern(base_name)
        print(base_name, " Keywords: ", keywords)
        file_object = FileObject(os.path.join(parent_path, dir_entry.name), file_type,
                '', False)  # Future can generate some description
        file_name, _ = createName(folder_database._argument_database[file_type].name_dict.keys(), keywords)
        folder_database.add(file_type, keywords, file_object, file_name)

    def read(self, file_path, keyword_list, recursive=False, folder_database=None):
        """
        Load the file name specified and store it in history
        Parameters:
            file_path folder location
            keyword_list keywords used to describe the folder
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if folder_database is None:
            folder_database = TypeDatabase(data_type_list=[DataType.csv, DataType.image])
            create_result = True
        else:
            create_result = False

        if len(keyword_list) == 0:
            keyword_list = splitPattern(file_path)
        if not os.path.isdir(file_path):
            file_path = os.path.join(os.path.expanduser('~'),
                                     file_path)
            if not os.path.isdir(file_path):
                print("Cannot find folder: ", file_path)
                return result_object
        for dir_entry in os.scandir(file_path):
            if self.checkEndsWith(dir_entry.name, ['.csv','.xlsx']) and dir_entry.is_file():
                self.addFile(dir_entry, DataType.csv, folder_database, file_path)
            elif self.checkEndsWith(dir_entry.name, ['.png', '.jpg', '.JPG', '.jpeg']) and dir_entry.is_file():
                self.addFile(dir_entry, DataType.image, folder_database, file_path)
            if recursive and dir_entry.is_dir():
                dir_keywords = splitPattern(dir_entry.name)
                self.read(os.path.join(file_path, dir_entry.name), keyword_list + dir_keywords, True, folder_database)
        if not create_result:
            return False
        folder_object = FolderObject(folder_database, file_path)
        result_object = ResultObject(folder_object, keyword_list, DataType.folder, CommandStatus.Success)
        result_object.createName(keyword_list)
        return result_object
