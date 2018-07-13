#!/usr/bin/env python
"""
Define load command
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from Alfarvis.history.keyword_search import KeywordSearch
from .abstract_command import AbstractCommand
from .argument import Argument


class ListHistory(AbstractCommand):
    """
    List all variables in history
    """

    def __init__(self):
        self.datatype_keyword_search = KeywordSearch()
        data_types = DataType.__members__
        self.data_keys = list(data_types.keys())
        for i, key in enumerate(self.data_keys):
            if key not in ["history", "user_string", "user_conversation"]:
                self.datatype_keyword_search.add(key.split('_'), i)

    def commandTags(self):
        """
        return tags that are used to identify load command
        """
        return ["list", "history", "variables"]

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
        user_data_indices = self.datatype_keyword_search.search(
                user_conv.data, use_max_hit=False)
        user_data_types = [DataType[self.data_keys[i]] for i in user_data_indices]
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
                    print(row_format.format(object_name, keywords, data_type.name))
        except:
            result_object = ResultObject(None, None, None, CommandStatus.Error)

        return result_object
