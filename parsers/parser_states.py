#!/usr/bin/env python
"""
Different states that our parser can take
"""

from enum import Enum

class ParserStates(Enum):
    command_unknown = 1
    command_known = 2
    command_known_data_unknown = 3
    command_known_data_known = 4
    end = 5



