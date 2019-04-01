#!/usr/bin/env python
from .data_object import DataObject
from .pattern_split import splitPattern
from .file_name_object import FileObject
from .data_type import DataType
import os


def createFileObjectFromName(file_to_load):
    base_name = os.path.basename(file_to_load)
    splits = os.path.splitext(base_name)
    ext = splits[-1]
    if ext == '.png' or ext == '.jpg':
        file_type = DataType.image
    elif ext == '.csv' or ext == '.xls' or ext == '.xlsx':
        file_type = DataType.csv
    elif ext == '.alfa':
        file_type = DataType.alpha_script
    else:
        return None
    file_object = FileObject(file_to_load, file_type, 'User loaded input file', False)
    keywords = splitPattern(splits[0])
    return DataObject(file_object, keywords, DataType.file_name)
