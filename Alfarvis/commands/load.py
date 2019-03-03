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

    def briefDescription(self):
        return "Load dataset/image/figure"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def __init__(self):
        self.reader_dictionary = create_reader_dictionary()

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["load", "import", "open"]

    @property
    def run_in_background(self):
        return True

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        return [Argument(keyword="file_name", optional=False,
                         argument_type=[DataType.file_name,
                                        DataType.figure])]

    def preEvaluate(self, file_name):
        """
            For readers that allow run in background
        """
        if (file_name.data_type is not DataType.figure and
            (not file_name.data.loaded or
                file_name.data.data_type is DataType.algorithm_arg) and
            os.path.isfile(file_name.data.path) and
            file_name.data.data_type in self.reader_dictionary and
            self.reader_dictionary[file_name.data.data_type].read_in_background):
            print("Reader status: ", self.reader_dictionary[file_name.data.data_type].read_in_background)
            reader = self.reader_dictionary[file_name.data.data_type]
            parallel_result = reader.preRead(file_name.data.path,
                                             file_name.keyword_list)
            return parallel_result
        return ResultObject(None, None, None, CommandStatus.Success)

    def evaluate(self, file_name, pre_evaluate_results=None):
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
            if type(file_name.data) == list:
                win = file_name.data[0]
            else:
                win = file_name.data
            VizContainer.current_figure = win.gcf()
            win.show()
            return ResultObject(None, None, None, CommandStatus.Success)

        if file_name.data.loaded and file_name.data.data_type is not DataType.algorithm_arg:
            Printer.Print("File already loaded!")
            return ResultObject(None, None, None, CommandStatus.Success)

        if os.path.isfile(file_name.data.path):
            data_type = file_name.data.data_type
            if data_type in self.reader_dictionary:
                reader = self.reader_dictionary[data_type]
                if reader.read_in_background:
                    result_object = reader.read(file_name.data.path,
                                                file_name.keyword_list, pre_evaluate_results)
                else:
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

    def ArgNotFoundResponse(self, file_name):
        super().ArgNotFoundResponse(file_name, 'file', 0)

    def MultipleArgsFoundResponse(self, file_name):
        super().MultipleArgsFoundResponse(file_name, 'files', 0)
