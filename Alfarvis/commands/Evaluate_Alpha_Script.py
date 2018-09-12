#!/usr/bin/env python
"""
Run a script written in alfarvis language
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.alpharvis_versions import create_alpha_module_dictionary


class Evaluate_AlphaScript(AbstractCommand):
    """
    Evaluate a script written in alpharvis
    """

    def briefDescription(self):
        return "Evaluate a script written in ALFARVIS"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning

    def commandTags(self):
        """
        Tags to identify the command
        """
        return ["evalate","execute"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="alpha_script", optional=False,
                         argument_type=DataType.alpha_script, number=1)]

    def evaluate(self, alpha_script):
        """
        Run an alfarvis script
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        alpha_module_dictionary = create_alpha_module_dictionary()
        latest_version = max(alpha_module_dictionary.keys())
        alpha = alpha_module_dictionary[latest_version]()
        # Get the lines
        lines = alpha_script.data
        for line in lines:
            alpha(line)
        
        result_object = ResultObject(None, None, None, CommandStatus.Success)

        return result_object
