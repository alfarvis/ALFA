#!/usr/bin/env python2

from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum

class CommandStatus(Enum):
    Success = 1
    Error = 2

class AbstractCommand(object):
    __metaclass__ = ABCMeta
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
    def verifyArguments(self, *args):
        """
        Check the arguments passed for evaluate
        to have the correct types.

        Returns true if arguments are of valid type
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
