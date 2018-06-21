#!/usr/bin/env python
from Alfarvis.history import Database
from . import abstract_command
from Alfarvis.basic_definitions.get_subclasses import get_subclasses


def create_command_database():
    """
    Create a database of the available commands that are
    sub-class of AbstractCommand. The command can be searched
    using keywords as in
        matched_commands = command_database.search([list_of_key_words])

    Returns - a keyword searchable database of available commands
    """
    command_database = Database()
    for cls in get_subclasses(abstract_command.AbstractCommand):
        cls_instance = cls()
        command_database.add(cls_instance.commandTags(), cls_instance)
    return command_database
