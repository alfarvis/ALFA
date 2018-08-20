#!/usr/bin/env python
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern)
from Alfarvis.history.data_base import Database
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer, TablePrinter, Align


class ListCommands(AbstractCommand):
    """
    List all variables in history
    """

    def briefDescription(self):
        return "List all available commands"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def __init__(self):
        self.commandtype_database = Database()
        for command_type in AbstractCommand.CommandType:
            keywords = splitPattern(command_type.name)
            keywords.append(command_type.name.lower())
            command_name = '.'.join(keywords)
            self.commandtype_database.add(keywords, command_type, name=command_name)

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["list", "commands", "statistics", "machine learning",
                "data handling", "visualization"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        return [Argument(keyword="history", optional=False,
                         argument_type=DataType.history),
                Argument(keyword="user_conv", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, history, user_conv):
        """
        Takes in the session history and prints all the elements stored in each
        category
        """
        result_object = ResultObject(None, None, None, CommandStatus.Success)
        if not hasattr(history.data, 'command_database'):
            Printer.Print("History does not contain command database")
            return result_object
        command_database = history.data.command_database
        TablePrinter.initialize(4, [20, 20, 30, 55], ['Command Name', 'Command type',
                                'Keywords', 'Description'],
                               [Align.Right, Align.Center, Align.Center,
                                Align.Left])
        user_input = user_conv.data
        user_command_types = [data_object.data for data_object in
                              self.commandtype_database.search(user_input)]
        try:
            for command_data_object in command_database.data_objects:
                command_object = command_data_object.data
                command_type = command_object.commandType()
                if user_command_types != [] and command_type not in user_command_types:
                    continue
                if command_data_object.name is None:
                    if len(command_data_object.keyword_list) == 0:
                        object_name = "None"
                    else:
                        object_name = command_data_object.keyword_list[0]
                else:
                    object_name = command_data_object.name
                command_type_name = command_type.name.lower()
                command_tags = ' '.join(command_object.commandTags()[:2])
                command_brief = command_object.briefDescription()
                TablePrinter.addRow((object_name, command_type_name,
                                     command_tags, command_brief))
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)
        TablePrinter.sort(1)  # Sort data by command type
        TablePrinter.show()

        return result_object
