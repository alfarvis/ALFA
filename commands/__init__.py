"""
Provide commands database available for alpharvis
to implement
"""
from Alfarvis.history import Database, TypeDatabase, session_history
import importlib
import os
import pkgutil

command_database = Database()

pkg_dir = os.path.dirname(__file__)

for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

for i, cls in enumerate(abstract_command.AbstractCommand.__subclasses__()):
    cls_instance = cls(session_history)
    command_database.add(cls_instance.commandTags(), cls_instance)
