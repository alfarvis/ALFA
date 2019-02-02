#!/usr/bin/env python3
"""
Provide abstract base class for implementing new commands
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from Alfarvis.printers import Printer
from enum import Enum
import string
import random


class AbstractCommand(object):
    """
    Base class for new commands. Provides virtual
    functions to be implemented by new commands
    """
    __metaclass__ = ABCMeta

    class CommandType(Enum):
        DataHandling = 1,
        Statistics = 2,
        Visualization = 3,
        MachineLearning = 4
        Unknown = 5

    @abstractproperty
    def commandTags(self):
        """
        Return a list of strings that
        identify the command among
        a list of commands
        """
        pass

    @abstractproperty
    def commandName(self):
        """
        Returns a unique name for the command
        """
        pass

    @abstractmethod
    def briefDescription(self):
        return "No description provided"

    @abstractmethod
    def example(self, history, user_conv):
        return "No example available"

    @abstractmethod
    def commandType(self):
        """
        Return command type
        """
        return self.CommandType.Unknown

    @abstractproperty
    def argumentTypes(self):
        """
        Return a list of argument objects.
        The argument object provides
        argument types, argument tags etc.
        For example, a load command expects
        argument to be a string. Similarly,
        the mean command requires the argument
        to be a matrix of n>=1 dimensions
        """
        pass

    @abstractmethod
    def evaluate(self, *args):
        """
        Evaluate the command using the arguments
        passed

        Returns ResultObject with result and any errors
        """
        pass

    def random_generator(self, size=6, chars=string.ascii_lowercase):
        """
        Generate random keywords of specified size
        """
        return ''.join(random.choice(chars) for x in range(size))

    def ArgNotFoundResponse(self, arg_name, data_name='variable(s)', tag_ind=-1):
        Printer.Print("Couldn't find the ", data_name, " you are looking for...")
        Printer.Print("Which file do you want me to ", self.commandTags[ind], "?")

    def ArgFoundResponse(self, arg_name):
        # Will only be called for command with multiple arg types
        Printer.Print("Found variable")

    def MultipleArgsFoundResponse(self, arg_name, data_name='variables', tag_ind=-1):
        Printer.Print("I found multiple ", data_name, " that seem to match your query")
        Printer.Print("Could you please look at the following", data_name, "and tell me which one you "
                "want to ", self.commandTags[tag_ind], "?")

    def AnalyzeArgNotFoundResponse(self, arg_name, keyword='analyze'):
        Printer.Print("Which variable do you want me to ", keyword, "?")

    def AnalyzeMultipleArgsFoundResponse(self, arg_name, keyword='analyze'):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to ", keyword, "?")

    def DataMineArgNotFoundResponse(self, arg_name):
        if arg_name == "data_frame":
            Printer.Print("Which data frame do you want me to classify?")
        else:
            Printer.Print("Which classifiers do you want me to test?")

    def DataMineArgFoundResponse(self, arg_name):
        if arg_name == "data_frame":
            Printer.Print("Found the data frame")
        else:
            Printer.Print("Found the classification models to test")

    def DataMineMultipleArgsFoundResponse(self, arg_name):
        if arg_name == "data_frame":
            Printer.Print("I found multiple data frames that seem to match your query")
            Printer.Print("Could you please look at the following data frames and tell me which one you "
                  "want to classify?")

    def addCommandToKeywords(self, keyword_set):
        """
        Add command tags to keyword set
        """
        tags = self.commandTags()
        tags_added = False
        for tag in tags:
            if tag not in keyword_set:
                tags_added = True
                keyword_set.add(tag)
                break
        # If command tags not found try adding result tag
        # if result already present, try adding secondary
        for tag in ["result", "secondary"]:
            if not tags_added and tag not in keyword_set:
                tags_added = True
                keyword_set.add(tag)
                break
        if not tags_added:
            Printer.Print("Could not find a unique tag",
                          "to add to the keyword_set")
            Printer.Print("Adding a random string")
            keyword_set.add(self.random_generator())
