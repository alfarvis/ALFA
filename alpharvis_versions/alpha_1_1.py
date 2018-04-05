#!/usr/bin/env python2
"""
Defines alpha 1.0
"""

from .abstract_alpha import AbstractAlpha
from Alfarvis.parsers.parser_class import AlfaDataParser
from Alfarvis.commands.load_file_database import LoadDatabase
from Alfarvis import package_directory
from Alfarvis.basic_definitions import DataObject, DataType
import os


def add_basic_database(history):
    data_base_path = os.path.join(package_directory,
                                  'resources/file_database.csv')
    if os.path.isfile(data_base_path):
        cmd = LoadDatabase()
        data_base_object = DataObject('file_database.csv',
                                      ['basic', 'database'])
        history.add(DataType.data_base, data_base_object.keyword_list,
                    data_base_object)
        results = cmd.evaluate(data_base_object)
        if type(results) == list:
            for result in results:
                history.add(result.data_type, result.keyword_list,
                            result.data_object)
            print("Loaded basic file database")
        else:
            print ("Failed to load file database")


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
        add_basic_database(self.parser.history)

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
