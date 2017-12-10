#!/usr/bin/env python2

from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractAlpha(object):
    __metaclass__ = ABCMeta
    @abstractproperty
    @classmethod
    def _get_version(self):
        """
        Version of the alpha class a double with
        major and minor versions such (1.0) where
        1 is the major version and 0 is the minor
        version. This version allows us to identify
        different alpha's and load them into a dictionary.
        """
        pass

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
