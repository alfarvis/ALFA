#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus
from Alfarvis.windows import Window
from skimage.io import imread
import matplotlib.pyplot as plt


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

        win = Window.window()
        #f = win.gcf()
        plt.imshow(data)
        plt.gca().axis('off')
        win.show()
        # Initialize image manipulation command group
        result = ResultObject(data, keyword_list, DataType.image,
                              CommandStatus.Success, add_to_cache=True)
        result.createName(keyword_list)
        return result
