#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
from skimage.io import imread


class ReadImage(AbstractReader):

    @classmethod
    def data_type(self):
        return DataType.image

    def read(self, file_path, keyword_list):
        try:
            data = imread(file_path)
        except:
            return ResultObject(None, None, None,
                                command_status=CommandStatus.Error)
        # Initialize image manipulation command group
        return ResultObject(data, keyword_list, DataType.image,
                            CommandStatus.Success, add_to_cache=True)
