#!/usr/bin/env python
"""
Define save previous result command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument


class SavePreviousResult(AbstractCommand):
    """
    List all variables in history
    """

    def commandTags(self):
        """
        return tags that are used to identify save previous result command
        """
        return ["save", "previous", "result"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the save previous result command
        """
        return [Argument(keyword="history", optional=False,
                         argument_type=DataType.history),
                Argument(keyword="name", optional=False,
                         tags=[Argument.Tag('as', 1), Argument.Tag('into', 1)],
                         argument_type=DataType.user_string)]

    def evaluate(self, history, name):
        """
        Saves the last element from history and saves it with given name
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        try:
            previous_result = history.getLastObject()
            name_lower = name.data.lower()
            keyword_list = name_lower.split(' ')
            print("Last data type: ", history.last_data_type)
            result_object = ResultObject(
                previous_result.data, keyword_list, history.last_data_type,
                CommandStatus.Success)
        except RuntimeError:
            print("Cannot find last object from history")

        return result_object
