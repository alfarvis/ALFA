#!/usr/bin/env python
from .abstract_reader import AbstractReader
from Alfarvis.basic_definitions import DataType, ResultObject, CommandStatus, DataObject
from Alfarvis.commands.Stat_ListColumns import StatListColumns
from Alfarvis.commands.Stat_Container import StatContainer
from Alfarvis.printers import Printer
from Alfarvis.windows import PropertyEditor
import pandas as pd
import re
import numpy as np
from Alfarvis.Toolboxes.DataGuru import DataGuru


class ReadAlgo(AbstractReader):

    @classmethod
    def data_type(self):
        return DataType.algorithm_arg

    def createProperties(self, file_path):
        data = pd.read_csv(file_path)
        properties = {}
        for column in data.columns:
            if column == 'Model':
                continue
            column_data = data[column][0]
            if column_data == 'TRUE':
                column_data = True
            elif column_data == 'False':
                column_data = False
            elif column_data == None:
                column_data = "None"
            properties[str(column)] = column_data
        return properties, str(data['Model'][0])

    def updateModel(self, result_data):
        properties = result_data[1]
        model_name = result_data[2]
        print("Properties: ", properties)
        result_data[0] = DataGuru.createModel(properties, model_name)

    def read(self, file_path, keyword_list):
        try:
            property_data, model_name = self.createProperties(file_path)
            model = DataGuru.createModel(property_data, model_name)
        except:
            Printer.Print("File not found")
            return ResultObject(None, None, None, CommandStatus.Error)

        command_status = CommandStatus.Success
        result_data = [model, property_data, model_name, self.updateModel]
        result_object = ResultObject(
            result_data, keyword_list, DataType.algorithm_arg, command_status,
            add_to_cache=True)
        result_object.createName(keyword_list)

        if (PropertyEditor.parent_widget is None or
            PropertyEditor.property_editor_class is None):
            Printer.Print("Cannot modify algorithm properties in non-GUI mode")
        else:
            property_editor = PropertyEditor.property_editor_class(result_object)
            PropertyEditor.addPropertyEditor(property_editor)

        return result_object
