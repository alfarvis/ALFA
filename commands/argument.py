#!/usr/bin/env python

from enum import Enum


class ArgumentType(Enum):
    image = 1
    csv = 2
    number = 3
    string = 4

class Argument(object):
    """
    Provides information about an argument:
        - Argument types
        - Argument tags
        - optional or not
        - keyword that is used in evaluation
    """

    def __init__(self, argument_type=ArgumentType.string, optional=True, keyword="", tags=[]):
        # If argument is optional, need not be provided by user
        self.optional = optional
        # Argument type also used to disambiguate the arguments
        self.argument_type = argument_type
        # Tags used for searching the argument
        self.tags = tags
        # Keyword used in function to identify the argument
        self.keyword = keyword
