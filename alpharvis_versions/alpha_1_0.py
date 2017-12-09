#!/usr/bin/env python2

from abstract_alpha import AbstractAlpha

class Alpha(AbstractAlpha):
    __version__ = 1.0
    def __call__(self, text):
        """
        Parse a provided text and return the  output in the form text
        Parameters:
            text - 'String input from user'
        Returns:
            output from Alpha
        """
        return "You Entered: " + text
