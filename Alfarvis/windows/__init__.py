"""
Provide commands database available for alpharvis
to implement
"""
import importlib
import os
import pkgutil
from .window_interface import Window

pkg_dir = os.path.dirname(__file__)

for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)
