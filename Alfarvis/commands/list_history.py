#!/usr/bin/env python
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument


class ListHistory(AbstractCommand):
    """
    List all variables in history
    """

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["list", "history"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the load command
        """
        return [Argument(keyword="history", optional=False,
                         argument_type=DataType.history)]

    def evaluate(self, history):
        """
        Takes in the session history and prints all the elements stored in each
        category
        """
        result_object = ResultObject(None, None, None, CommandStatus.Success)
        row_format = "{:>15} {:>35} {:>15}"
        print(row_format.format("Name", "Keywords", "Type"))
        try:
            for data_type, data_base in history.data._argument_database.items():
                for data_object in data_base.data_objects:
                    if data_object.name is None:
                        if len(data_object.keyword_list) == 0:
                            object_name = "None"
                        else:
                            object_name = data_object.keyword_list[0]
                    else:
                        object_name = data_object.name
                    keywords = " ".join(data_object.keyword_list)
                    print(row_format.format(object_name, keywords, data_type.name))
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
