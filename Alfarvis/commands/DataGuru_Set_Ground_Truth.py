#!/usr/bin/env python3
"""
Set ground truth
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
import numpy
import re


class SetGT(AbstractCommand):
    """
    Sets the ground truth for data guru operations
    """

    def commandTags(self):
        """
        return tags that are used to identify set ground truth command
        """
        return ["setgt", "set", "ground", "truth"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the set ground truth command
        """
        return [Argument(keyword="array_data", optional=False,
                         argument_type=DataType.array)]

    def evaluate(self, array_data):
        """
        Calculate average value of the array and store it to history
        Parameters:

        """
        StatContainer.ground_truth = array_data
        print ("Setting ground truth to ", " ".join(array_data.keyword_list))
        return ResultObject(None, None, None, CommandStatus.Success)
