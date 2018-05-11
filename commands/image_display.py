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
        try:
            plt.imshow(image.data)
            plt.show(block=False)
            print("Displaying image" + image.keyword_list[0])
            if image is not None:
                VarStore.SetCurrentImage(image.data, image.keyword_list[0])
            result_object = ResultObject(
                None, None, None, CommandStatus.Success)
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
