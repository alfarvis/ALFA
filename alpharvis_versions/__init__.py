"""
Provides dictionary of available alpha versions stored in this dictionary
"""
import importlib
import pkgutil
import os

alpha_module_dictionary = {}

pkg_dir = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)


for alpha_class in abstract_alpha.AbstractAlpha.__subclasses__():
    if alpha_class._get_version() in alpha_module_dictionary:
        print "Version conflict between: ", alpha_class, " and ", alpha_module_dictionary[alpha_class._get_version()]
        continue
    else:
        alpha_module_dictionary[alpha_class._get_version()] = alpha_class

print "Available alpha versions: ", alpha_module_dictionary.keys()
