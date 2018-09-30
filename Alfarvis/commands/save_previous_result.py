#!/usr/bin/env python
"""
Define save previous result command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer


class SavePreviousResult(AbstractCommand):
    """
    List all variables in history
    """

    def briefDescription(self):
        return "Rename variable as user specified name"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        return tags that are used to identify save previous result command
        """
        return ["save", "previous", "result", "save chat", "save notebook"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the save previous result command
        """
        return [Argument(keyword="history", optional=False,
                         argument_type=DataType.history),
                Argument(keyword="user_conv", optional=False,
                         argument_type=DataType.user_conversation),
                Argument(keyword="name", optional=True,
                         tags=[Argument.Tag('as', Argument.TagPosition.After),
                               Argument.Tag(
                             'into', Argument.TagPosition.After)],
                         argument_type=DataType.user_string, fill_from_cache=False)]

    def evaluate(self, history, user_conv, name=None):
        """
        Saves the last element from history and saves it with given name
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if 'notebook' in user_conv.data or 'chat' in user_conv.data:
            Printer.save(name)
            return ResultObject(None, None, None, CommandStatus.Success)
        if name is None:
            return result_object
        try:
            previous_result = history.data.getLastObject()
            name_lower = name.data.lower()
            keyword_list = name_lower.split(' ')
            result_object = ResultObject(
                previous_result.data, keyword_list,
                history.data.last_data_type,
                CommandStatus.Success)
            result_object.createName(keyword_list)
            Printer.Print("Saving ", ' '.join(previous_result.keyword_list), ' as ',
                  result_object.name)
        except RuntimeError:
            Printer.Print("Cannot find last object from history")

        return result_object
