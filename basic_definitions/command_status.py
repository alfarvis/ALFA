#!/usr/bin/env python2
"""
Defines command status
"""

from enum import Enum


class CommandStatus(Enum):
    """
    Return type after completing the
    evaluation of a command
    """
    Success = 1
    Error = 2
