#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus, DataObject
from Alfarvis.printers import Printer



class ReadAlphaScript(AbstractReader):

    @classmethod
    def data_type(self):
        return DataType.alpha_script

    def read(self, file_path, keyword_list):
        try:            
            lines = [line.rstrip('\n') for line in open(file_path)]
        except:
            Printer.Print("File not found")
            return ResultObject(None, None, None, CommandStatus.Error)

        command_status = CommandStatus.Success

        result_object = ResultObject(
            lines, keyword_list, DataType.alpha_script, command_status,
            add_to_cache=True)
        result_object.createName(keyword_list)

        return result_object
