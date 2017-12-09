from abstract_alpha import AbstractAlpha
import importlib
import os

alpha_module_dictionary = {}
alpha_module_name_dictionary = {}

print "Path: ", __path__
print "Name: ", __name__

prefix = __name__+'.'

for name in os.listdir(__path__[-1]):
    if (name.endswith(".py") and name != "__init__.py" and name != "abstract_alpha.py"):
        print "name: ", name
        module_name = name[:-3]
        try:
            alpha_module = importlib.import_module(__name__ + '.' + module_name)
        except ImportError:
            print "Cannot import module: ", module_name
            continue
        alpha_class = alpha_module.Alpha
        if issubclass(alpha_class, AbstractAlpha):
            if alpha_class.__version__ in alpha_module_dictionary:
                print "Version conflict between: ", module_name, " and ", alpha_module_name_dictionary[alpha_class.__version__]
                continue
            else:
                alpha_module_name_dictionary[alpha_class.__version__] = module_name
                alpha_module_dictionary[alpha_class.__version__] = alpha_class
        else:
            print "Specified alpha class is not a subclass of abstract alpha"

print "Available alpha versions: ", alpha_module_dictionary.keys()
