#!/usr/bin/env python
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.history.data_base import Database
from .abstract_command import AbstractCommand
from .argument import Argument


class ListHistory(AbstractCommand):
    """
    List all variables in history
    """

    def __init__(self):
        self.datatype_database = Database()
        for key in DataType.__members__:
            if key not in ["history", "user_string", "user_conversation"]:
                key_up = key.replace('_', '.')
                key_split = key.split('_')
                self.datatype_database.add(key_split, DataType[key],
                                           name=key_up)

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["list", "history", "variables", "array", "file"]

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
        row_format = "{:>15} {:>35} {:>15}"
        print(row_format.format("Name", "Keywords", "Type"))
        user_input = user_conv.data
        two_phrases = [" ".join(tup)for tup in
                       zip(user_input[:-1], user_input[1:])]
        user_input.extend(two_phrases)
        user_data_types = [data_object.data for data_object in
                           self.datatype_database.search(user_input)]
        try:
            for data_type, data_base in history.data._argument_database.items():
                if user_data_types != [] and data_type not in user_data_types:
                    continue
                for data_object in data_base.data_objects:
                    if data_object.name is None:
                        if len(data_object.keyword_list) == 0:
                            object_name = "None"
                        else:
                            object_name = data_object.keyword_list[0]
                    else:
                        object_name = data_object.name
                    keywords = " ".join(data_object.keyword_list)
                    data_type_name = data_type.name.replace('_', '.')
                    print(row_format.format(object_name, keywords,
                                            data_type_name))
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
