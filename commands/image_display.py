#!/usr/bin/env python2
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
#from Alfarvis.commands.read_data import ReadData
from Alfarvis.data_handlers import create_reader_dictionary
from .abstract_command import AbstractCommand
from .argument import Argument
import matplotlib.pyplot as plt
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore
import os


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
        return ["display", "image","show"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        #return []
        return [Argument(keyword="image", optional=False,
                         argument_type=DataType.image)]

    def evaluate(self, image):
        """
        Display the image specified            
        """
        
        #if image!=0:
        #kList=['Image','Image2']
        VarStore.SetCurrentImage(image.data,image.keyword_list[0])
        plt.imshow(VarStore.currImg)
        print("Displaying image"+ VarStore.currImg_name)
        result_object = ResultObject(None, None, None, CommandStatus.Success)


        return result_object
