#!/usr/bin/env python2
"""
Defines alpha 1.0
"""

from .abstract_alpha import AbstractAlpha
from Alfarvis.parsers.parser_class import AlfaDataParser

class Alphav1_1(AbstractAlpha):
    """
    Simple alpha that uses basic parser
    """
    __version__ = 1.1
    @classmethod
    def _get_version(self):
        """
        Return current version
        """
        return self.__version__

    def __init__(self):
        self.parser = AlfaDataParser()

    def __call__(self, text):
        """
        Parse a provided text and return the  output in the form text
        Parameters:
            text - 'String input from user'
        Returns:
            output from Alpha
        """
        self.parser.parse(text)
        return ''
