#!/usr/bin/env python2

from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum


class CommandStatus(Enum):
    Success = 1
    Error = 2


class AbstractCommand(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def commandTags(self):
        """
        Return a list of strings that
        identify the command among
        a list of commands
        """
        pass

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
        passed and stores any result in history

        Returns status of evaluation.
        """
        pass
