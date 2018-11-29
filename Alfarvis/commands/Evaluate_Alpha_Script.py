#!/usr/bin/env python
"""
Run a script written in alfarvis language
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer
from Alfarvis.parsers.parser_states import ParserStates


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
        return ["evalate", "execute"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the command
        """
        # TODO Add an argument for k = number of clusters
        return [Argument(keyword="alpha_script", optional=False,
                         argument_type=DataType.file_name, number=1),
                Argument(keyword="parent_parser", optional=False)]

    def evaluate(self, alpha_script, parent_parser):
        """
        Run an alfarvis script
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if alpha_script.data.data_type is not DataType.alpha_script:
            Printer.Print("File not of alpha script type: ", alpha_script.data.data_type)
            return result_object
        # Get the lines
        try:
            lines = [line.rstrip('\n') for line in open(alpha_script.data.path)]
        except:
            Printer.Print("Alpha script not found")
            return ResultObject(None, None, None, CommandStatus.Error)
        # Update parent parser state
        parent_parser.data.clearCommandSearchResults()
        for i, line in enumerate(lines):
            line = line.lstrip()
            print("Line: ", line)
            if len(line) == 0:
                continue
            elif line[0] == '#':
                continue  # Ignore comments
            parent_parser.data.parse(line)
            if parent_parser.data.currentState == ParserStates.command_known_data_unknown:
                Printer.Print("Ambiguous command at line: ", i)
                Printer.Print("Exiting script")
                break
        parent_parser.data.clearCommandSearchResults()
        result_object = ResultObject(None, None, None, CommandStatus.Success)

        return result_object

    def ArgNotFoundResponse(self,arg_name):
        Printer.Print("Which file do you want me to run?")
