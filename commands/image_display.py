#!/usr/bin/env python2
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.data_handlers import create_reader_dictionary
from .abstract_command import AbstractCommand
from .argument import Argument
import matplotlib.pyplot as plt
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore


class ImageDisplay(AbstractCommand):
    """
    Loads a csv file
    """

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

    def evaluate(self, image=None):
        """
        Display the image specified
        """
        if (image is None) and not hasattr(VarStore,'currImg'):
            print("No image provided to display")
            return ResultObject(None, None, None, CommandStatus.Error)
        try:
            if image is None:
                curr_image = VarStore.currImg
                image_name = VarStore.currImg_name
            else:
                curr_image = image.data
                image_name = image.keyword_list[0]
            plt.imshow(curr_image)
            plt.show(block=False)
            print("Displaying image" + image_name)
            if image is not None:
                VarStore.SetCurrentImage(image.data, image.keyword_list[0])
            result_object = ResultObject(
                None, None, None, CommandStatus.Success)
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
