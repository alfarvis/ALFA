#!/usr/bin/env python
from enum import Enum


class ArgumentType(Enum):
    image = 1
    csv = 2
    number = 3
    string = 4
    file_name = 5


