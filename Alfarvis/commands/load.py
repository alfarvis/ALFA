#!/usr/bin/env python
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.data_handlers import create_reader_dictionary
from .abstract_command import AbstractCommand
from .argument import Argument
from .Viz_Container import VizContainer
from Alfarvis.printers import Printer

import os


class Load(AbstractCommand):
    """
    Loads a csv file
    """

    def __init__(self):
        self.reader_dictionary = create_reader_dictionary()

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["load", "import", "open"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        return [Argument(keyword="file_name", optional=False,
                         argument_type=[DataType.file_name,
                                        DataType.figure])]

    def evaluate(self, file_name):
        """
        Load the file name specified and store it in history
        Parameters:
            file_name has two entries
                1. Path of the file to load
                2. Type of the file to load
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if file_name.data_type is DataType.figure:
            Printer.Print("Loading figure ", ' '.join(file_name.keyword_list))
            VizContainer.current_figure = file_name.data.gcf()
            file_name.data.show()
            return ResultObject(None, None, None, CommandStatus.Success)

        if file_name.data.loaded:
            Printer.Print("File already loaded!")
            return ResultObject(None, None, None, CommandStatus.Success)

        if os.path.isfile(file_name.data.path):
            data_type = file_name.data.data_type
            if data_type in self.reader_dictionary:
                reader = self.reader_dictionary[data_type]
                result_object = reader.read(file_name.data.path,
                                            file_name.keyword_list)
                Printer.Print("Loaded file: ",
                              os.path.basename(file_name.data.path))
                file_name.data.loaded = True
            else:
                Printer.Print("We cannot load ", data_type,
                              " yet! Please try again later")
        else:
            Printer.Print("File not found.\n Please make sure the file exists "
                          "in the specified location")
        return result_object
