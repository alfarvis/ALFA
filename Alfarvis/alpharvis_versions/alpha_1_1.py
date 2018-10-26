#!/usr/bin/env python2
"""
Defines alpha 1.0
"""

from .abstract_alpha import AbstractAlpha
from Alfarvis.parsers.parser_class import AlfaDataParser
from Alfarvis.data_handlers.read_database import ReadDatabase
from pathlib import Path
from Alfarvis.basic_definitions import DataObject, DataType
import os


def add_basic_database(history):
    data_base_path = os.path.join(str(Path.home()),
                                  'AlfaDatabase/file_database.csv')
    if os.path.isfile(data_base_path):
        reader = ReadDatabase()
        data_base_object = DataObject(data_base_path,
                                      ['startup', 'database'])
        history.add(DataType.data_base, data_base_object.keyword_list,
                    data_base_object)
        results = reader.read(data_base_object.data,
                              data_base_object.keyword_list)
        if type(results) == list:
            for result in results:
                history.add(result.data_type, result.keyword_list,
                            result.data, name=result.name)
            print("Loaded basic file database")
        else:
            print("Failed to load file database")


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
        self.history = self.parser.history

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
