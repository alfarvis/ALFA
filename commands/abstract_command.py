#!/usr/bin/env python2
"""
Provide abstract base class for implementing new commands
"""
from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractCommand(object):
    """
    Base class for new commands. Provides virtual
    functions to be implemented by new commands
    """
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
