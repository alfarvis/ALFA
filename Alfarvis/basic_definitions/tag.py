#!/usr/bin/env python3
from enum import Enum


class TagPosition(Enum):
    """
    Position of tag
    """
    Before = 1
    Around = 2
    After = 3


class Tag:
    """
    Tag class with name  and position
    """

    def __init__(self, name, position):
        self.name = name
        self.position = position
