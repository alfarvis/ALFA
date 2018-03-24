#!/usr/bin/env python
from Alfarvis.history import Database
from . import abstract_command

def create_command_database(session_history):
    """
    Create a database of the available commands that are
    sub-class of AbstractCommand. The command can be searched
    using keywords as in
        matched_commands = command_database.search([list_of_key_words])
    Parameters:
        session_history - TypeDatabase object that stores results of commands

    Returns - a keyword searchable database of available commands
    """
    command_database = Database()
    for i, cls in enumerate(abstract_command.AbstractCommand.__subclasses__()):
        cls_instance = cls(session_history)
        command_database.add(cls_instance.commandTags(), cls_instance)
    return command_database
