"""
Provide readers for loading data into history
"""
import importlib
import os
import pkgutil
from .create_reader_dictionary import create_reader_dictionary


pkg_dir = os.path.dirname(__file__)

for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)
