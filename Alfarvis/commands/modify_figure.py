#!/usr/bin/env python3
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.windows import PropertyEditor
from .abstract_command import AbstractCommand
from .argument import Argument
from .Viz_Container import VizContainer
from Alfarvis.printers import Printer


class ModifyFigure(AbstractCommand):

    def briefDescription(self):
        return "Modify properties of a figure"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def commandTags(self):
        return ["modify figure", "manipulate figure", "modify", "manipulate"]

    def argumentTypes(self):
        return [Argument(keyword="figure_object", optional=True,
                         argument_type=DataType.figure)]

    def evaluate(self, figure_object):
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if (PropertyEditor.parent_widget is None or
            PropertyEditor.property_editor_class is None):
            Printer.Print("Cannot modify figure in non-GUI mode")
            return result_object
        if type(figure_object.data) != list:
            Printer.Print("This figure cannot be modified yet!")
            return result_object
        figure_object.data[0].show()
        property_editor = PropertyEditor.property_editor_class(figure_object)
        PropertyEditor.addPropertyEditor(property_editor)
        result_object.command_status = CommandStatus.Success
        return result_object
