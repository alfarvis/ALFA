"""
Provides dictionary of available alpha versions stored in this dictionary
"""
import importlib
import pkgutil
import os
from .create_alpha_module_dictionary import create_alpha_module_dictionary


pkg_dir = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)
