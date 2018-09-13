#!/usr/bin/env python
from .data_type import DataType


def findFileTypes(user_conv):
    file_types = []
    for pattern in ['png', 'jpg', 'image', 'picture', 'pic']:
        if pattern in user_conv:
            file_types.append(DataType.image)
            break

    for pattern in ['csv', 'data']:
        if pattern in user_conv:
            file_types.append(DataType.csv)
            break

    if len(file_types) == 0:
        file_types = [DataType.image, DataType.csv]
    return file_types


def searchFileFromFolder(user_conv, history):
    folder_res = history.search(DataType.folder, user_conv)
    file_types = findFileTypes(user_conv)
    file_res = []
    for folder in folder_res:
        for file_type in file_types:
            file_res = file_res + folder.data.file_name_database.search(file_type, user_conv)
    if len(file_res) == 0:
        # Search all available folders
        for folder in history._argument_database[DataType.folder].data_objects:
            for file_type in file_types:
                file_res = file_res + folder.data.file_name_database.search(file_type, user_conv)
    return file_res
