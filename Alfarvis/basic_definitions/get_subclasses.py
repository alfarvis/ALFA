#!/usr/bin/env python


def get_subclasses(cls):
    """
    Get all subclasses recursively
    """
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass
