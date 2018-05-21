#!/usr/bin/env python2
"""
Create a dictionary of alpha modules
"""
from . import abstract_alpha

def create_alpha_module_dictionary():
    """
    Iterate through sub-classes of abstract alpha and
    create a dictionary based on version of alpha module.
    The alpha module can be recovered from the dictionary
    using the version of the alpha module (__version__)
    """
    alpha_module_dictionary = {}
    for alpha_class in abstract_alpha.AbstractAlpha.__subclasses__():
        if alpha_class._get_version() in alpha_module_dictionary:
            print ("Version conflict between: ",
                    alpha_class, " and ",
                    alpha_module_dictionary[alpha_class._get_version()])
            continue
        else:
            alpha_module_dictionary[alpha_class._get_version()] = alpha_class
    print("Available alpha versions: ", alpha_module_dictionary.keys())
    return alpha_module_dictionary
