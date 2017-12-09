#!/usr/bin/env python2

from abc import ABCMeta, abstractmethod

class AbstractAlpha(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __call__(self, text):
        """
        Parse a provided text and return the  output in the form text
        Parameters:
            text - 'String input from user'
        Returns:
            output from Alpha
        """
        pass
