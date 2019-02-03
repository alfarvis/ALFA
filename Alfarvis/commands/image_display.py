#!/usr/bin/env python3
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.windows import Window
from Alfarvis.data_handlers import create_reader_dictionary
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
from skimage.io import imread
import matplotlib.pyplot as plt
import os


class ImageDisplay(AbstractCommand):
    """
    image display
    """

    def briefDescription(self):
        return "display an image"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling
    
    def commandName(self):
        return "image.display"

    def __init__(self):
        self.reader_dictionary = create_reader_dictionary()

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["display", "show"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        # return []
        return [Argument(keyword="image", optional=True,
                         argument_type=[DataType.image,
                                        DataType.file_name])]

    def evaluate(self, image):
        """
        Display the image specified
        """
        try:
            if image.data_type is DataType.file_name:
                file_path = image.data.path
                if not os.path.isfile(file_path):
                    Printer.Print("Cannot find image file: ", file_path)
                    raise RuntimeError
                curr_image = imread(file_path)
                result_object = ResultObject(
                    curr_image, image.keyword_list, DataType.image, CommandStatus.Success)
            else:
                curr_image = image.data
                result_object = ResultObject(
                    None, None, None, CommandStatus.Success)
            image_name = image.keyword_list[0]
            win = Window.window()
            plt.imshow(curr_image)
            plt.gca().axis('off')
            win.show()
            Printer.Print("Displaying image" + image_name)
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
