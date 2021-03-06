#!/usr/bin/env python
"""
Provides definition of argument for a command
"""
from Alfarvis.basic_definitions import (DataType, Tag, TagPosition)
from collections import namedtuple


class Argument(object):
    """
    Provides information about an argument:
        - Argument types
        - Argument tags
        - optional or not
        - keyword that is used in evaluation
    """
    Tag = Tag
    TagPosition = TagPosition

    def __init__(self, argument_type=DataType.string, optional=True, keyword="", tags=[],
                 number=1, fill_from_cache=True):
        """
        Constructor
        """
        # If argument is optional, need not be provided by user
        self.optional = optional
        # Argument type also used to disambiguate the arguments
        self.argument_type = argument_type
        # Tags used for searching the argument
        self.tags = tags
        # Keyword used in function to identify the argument
        self.keyword = keyword
        # The number of arguments of this argument type
        self.number = number
        # If optional is true, fill from cache fills the argument
        # based on the last element in history
        self.fill_from_cache = fill_from_cache
