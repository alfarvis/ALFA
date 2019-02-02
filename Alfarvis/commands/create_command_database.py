#!/usr/bin/env python
from Alfarvis.history import Database
from . import abstract_command
from Alfarvis.basic_definitions.get_subclasses import get_subclasses
from Alfarvis.basic_definitions.create_name import createName


def create_command_database():
    """
    Create a database of the available commands that are
    sub-class of AbstractCommand. The command can be searched
    using keywords as in
        matched_commands = command_database.search([list_of_key_words])

    Returns - a keyword searchable database of available commands
    """
    command_name_set = set()
    command_database = Database()
    for cls in get_subclasses(abstract_command.AbstractCommand):
        cls_instance = cls()
        split_tags = sum([tag.split(' ') for tag
                          in cls_instance.commandTags()], [])
        try:
            name = cls_instance.commandName()
        except:
            name, _ = createName(command_name_set, split_tags)
            
        command_database.add(cls_instance.commandTags(), cls_instance, name=name)
        command_name_set.add(name)
    return command_database
