#!/usr/bin/env python2
"""
Provide abstract base class for implementing new commands
"""
from abc import ABCMeta, abstractmethod, abstractproperty
import string
import random


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
        passed

        Returns ResultObject with result and any errors
        """
        pass

    def random_generator(self, size=6, chars=string.ascii_lowercase):
        """
        Generate random keywords of specified size
        """
        return ''.join(random.choice(chars) for x in range(size))

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
            print("Could not find a unique tag",
                  "to add to the keyword_set")
            print("Adding a random string")
            keyword_set.add(self.random_generator())
