#!/usr/bin/env python2
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.data_handlers import create_reader_dictionary
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
import matplotlib.pyplot as plt


class ImageDisplay(AbstractCommand):
    """
    Loads a csv file
    """

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

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
                         argument_type=DataType.image)]

    def evaluate(self, image):
        """
        Display the image specified
        """
        try:
            curr_image = image.data
            image_name = image.keyword_list[0]
            plt.imshow(curr_image)
            plt.show(block=False)
            Printer.Print("Displaying image" + image_name)
            result_object = ResultObject(
                None, None, None, CommandStatus.Success)
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
