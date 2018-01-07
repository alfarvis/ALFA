from Alfarvis.history import KeywordSearch
import importlib
import os
import pkgutil

command_search = KeywordSearch()
command_objects = []

pkg_dir = os.path.dirname(__file__)

for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

for i, cls in enumerate(abstract_command.AbstractCommand.__subclasses__()):
    cls_instance = cls()
    command_objects.append(cls_instance)
    command_search.add(cls_instance.commandTags(), i)
