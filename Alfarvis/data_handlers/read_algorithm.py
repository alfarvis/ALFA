#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus, DataObject
from Alfarvis.commands.Stat_ListColumns import StatListColumns
from Alfarvis.commands.Stat_Container import StatContainer
from Alfarvis.printers import Printer
import pandas as pd
import re
import numpy as np
from Alfarvis.Toolboxes.DataGuru import DataGuru


class ReadAlgo(AbstractReader):

    @classmethod
    def data_type(self):
        return DataType.algorithm_arg

    def read(self, file_path, keyword_list):
        try:
            model = DataGuru.readAlgorithm(file_path)
        except:
            Printer.Print("File not found")
            return ResultObject(None, None, None, CommandStatus.Error)

        command_status = CommandStatus.Success

        result_object = ResultObject(
            model, keyword_list, DataType.algorithm_arg, command_status,
            add_to_cache=True)
        result_object.createName(keyword_list)

        return result_object
