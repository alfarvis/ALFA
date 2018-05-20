#!/usr/bin/env python2
"""
Defines alpha 1.0
"""

from .abstract_alpha import AbstractAlpha

class Alpha(AbstractAlpha):
    """
    Simple alpha that just repeats
    whatever is input
    """
    __version__ = 1.0
    @classmethod
    def _get_version(self):
        """
        Return current version
        """
        return self.__version__

    def __call__(self, text):
        """
        Parse a provided text and return the  output in the form text
        Parameters:
            text - 'String input from user'
        Returns:
            output from Alpha
        """
        return "You Entered: " + text
