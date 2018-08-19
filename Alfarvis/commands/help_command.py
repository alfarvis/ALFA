#!/usr/bin/env python
"""
Help command
"""

from Alfarvis.basic_definitions import DataType, findClosestMatch
from Alfarvis.printers import Printer


def helpCommand(user_conv, history):
    """
    Provide help regarding commands/ program
    """
    try:
        user_conv.remove('how')
    except:
        pass
    # If general help then explain what
    # the program is how to use help etc
    # Check for arrays/ images in text
    array_res = history.search(DataType.array, user_conv)
    # Search for any commands
    command_res = history.command_database.search(user_conv)
    original_len = len(command_res)
    closest_res = findClosestMatch(command_res)
    if closest_res is not None:
        command_res = [closest_res]
    if 'visualize' in user_conv or ('plot' in user_conv and original_len > 1):
        Printer.Print("There are several visualization commands!")
        Printer.Print('you can get a list of them using "list visualization commands"')
        if len(array_res) >= 1:
            array_name = array_res[0].name
        else:
            array_name = '[array_name/keywords]'
        Printer.Print('For example, you can say "pie plot ' + array_name + '" to get a pie plot of array')
        Printer.Print('You can also use the command name if there is ambiguity in which command to use')
        Printer.Print('For example, you can also use "pie.plot ' + array_name + '" to get a pie plot of array')
        return
    # If no commands Just general help
    if len(command_res) >= 1:
        for command in command_res:
            Printer.Print('Providing help for command: ' + command.name)
            Printer.Print('Description: ')
            Printer.Print(command.data.briefDescription())
            Printer.Print('Example: ')
            Printer.Print(command.data.example(history, user_conv))
    else:
        Printer.Print('Alfa is data exploration and analysis software that uses natural language')
        Printer.Print('To begin data exploration, you should first load a dataset using the "load command". For example "load tour de france dataset" to load a cycling dataset')
        Printer.Print('To get a list of datasets that can be loaded, call "list files"')
        Printer.Print('Once you have loaded a dataset, you can perform different sets of commands : visualization, statistics, machine learning')
        Printer.Print('You can list commands using "list commands" or "list visualization/statistics... commands" for specific command list')
        Printer.Print('You can also get individual help for each of the commands by calling "help [command name]"')
        Printer.Print('Apart from the above commands, there are also data handling commands that can set row labels, set reference for setting legends etc')
        Printer.Print('You can get a list of data handling commands by calling "list data handling commands"')
