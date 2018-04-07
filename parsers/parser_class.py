from .parser_states import ParserStates
from Alfarvis.commands import create_command_database
from Alfarvis.history import TypeDatabase
from Alfarvis.basic_definitions import CommandStatus


class AlfaDataParser:

    def __init__(self):
        self.textInput = ""
        self.history = TypeDatabase()
        self.command_database = create_command_database()  # Command database
        self.clearCommandSearchResults()

    def clearCommandSearchResults(self):
        """
        Clear keyword list and command search result
        """
        self.currentState = ParserStates.command_unknown  # Parser state
        self.keyword_list = []  # Keywords extracted from input text
        # If a command is currently being parsed, resolve arguments for that
        # command
        self.command_search_result = []
        self.argumentsFound = {}  # Resolved arguments to separate from unresolved args
        self.argument_search_result = {}  # To resolve argument search results

    @classmethod
    def findIntersection(self, list1, list2):
        return set(list1).intersection(set(list2))

    def printCommands(self, command_list):
        print("Found multiple commands. Please select one of the commands")
        for command in command_list:
            print(command.keyword_list[0])

    def command_parse(self, text):
        """
        Parse an input from user to resolve commands
        Logic:
            IF command search already has results:
            ELSE:
               Search input forcommands
               if multiple commands found,
                   add to command search result
                   and resolve based on more user input
               else if single command found:
                   change parser state,
                   set current command
                   and start resolve arguments
               else if no command found:
                   return                
        """
        split_text = text.split(" ")
        if len(self.command_search_result) > 0:
            # If old text is used, we will not be able to resolve command
            # Since there will be multiple commands always
            res = self.command_database.search(split_text)
        else:
            # Tokenize text
            self.keyword_list = self.keyword_list + split_text
            res = self.command_database.search(self.keyword_list)
        if len(res) == 0:
            print("Command not found")
            print(
                "If you would like to know about existing commands, please say Find commands or Please help me")
            self.clearCommandSearchResults()
        elif len(res) == 1:
            self.foundCommand(res[0])
        else:
            if len(self.command_search_result) > 0:
                intersection_set = self.findIntersection(
                    self.command_search_result, res)
                if len(intersection_set) == 0:
                    self.command_search_result = res
                    print("The new commands do not match with the old input.")
                elif len(intersection_set) == 1:
                    self.foundCommand(intersection_set.pop())
                else:
                    self.command_search_result = list(intersection_set)
                    self.printCommands(self.command_search_result)
            else:
                self.command_search_result = res
                self.printCommands(self.command_search_result)

    def foundCommand(self, res):
        print("Found command", res.keyword_list[0])
        self.currentState = ParserStates.command_known
        self.currentCommand = res.data
        self.resolveArguments(self.keyword_list)

    def arg_reparse(self, text):
        # Tokenize text
        # Resolve arguments or data
        split_text = text.split(" ")
        if 'quit' in split_text:
            self.clearCommandSearchResults()
        else:
            self.resolveArguments(split_text)

    def resolveArguments(self, key_words):
        all_arg_names = set()
        argumentTypes = self.currentCommand.argumentTypes()
        for i in range(len(argumentTypes)):
            # TODO Try to use information from user when command gives error
            # TODO If user wants to substitute arguments in the process of resolution then ask him for confirmation.
            # TODO Handle multiple arguments with same type
            # TODO Handle arguments from keywords
            # TODO Handle composite commands (resolveCommands similar to
            # resolveArguments)
            arg_type = argumentTypes[i].argument_type
            arg_name = argumentTypes[i].keyword
            if arg_name in self.argumentsFound:
                continue
            data_res = self.history.search(arg_type, key_words)
            all_arg_names.add(arg_name)
            if len(data_res) == 1:
                self.argumentsFound[arg_name] = data_res[0]
            elif len(data_res) > 1:
                if arg_name in self.argument_search_result:
                    intersection_set = self.findIntersection(self.argument_search_result[arg_name],
                                                             data_res)
                    if len(intersection_set) == 0:
                        self.argument_search_result[arg_name] = data_res
                    elif len(intersection_set) == 1:
                        self.argumentsFound[
                            arg_name] = intersection_set.pop()
                    else:
                        self.argument_search_result[
                            arg_name] = list(intersection_set)
                else:
                    self.argument_search_result[arg_name] = data_res
        if len(argumentTypes) == len(self.argumentsFound):
            self.currentState = ParserStates.command_known_data_known
            self.argument_search_result = {}
            self.executeCommand(self.currentCommand, self.argumentsFound)
        else:
            self.currentState = ParserStates.command_known_data_unknown
            unknown_args = all_arg_names.difference(
                set(self.argumentsFound.keys()))
            # Get a list of unknown arguments"
            print("Cannot find some arguments", unknown_args)

    def executeCommand(self, command, arguments):
        # Execute command and take action based on result
        results = command.evaluate(**arguments)
        if type(results) == list:
            for result in results:
                self.addResultToHistory(result)
        else:
            self.addResultToHistory(results)

    def addResultToHistory(self, result):
        if result.command_status == CommandStatus.Error:
            self.currentState = ParserStates.command_known_data_unknown
            # TODO Find which arguments are wrong and resolve only those data
        elif result.command_status == CommandStatus.Success:
            # TODO Add a new function to add result to history
            self.history.add(result.data_type, result.keyword_list,
                             result.data)
            self.currentState = ParserStates.command_unknown
            self.clearCommandSearchResults()

    def parse(self, textInput):
        """
        Take input from user and resolve/run the instructions
        """
        # Tokenizer and create keyword list
        if self.currentState == ParserStates.command_unknown:
            self.command_parse(textInput)
        elif self.currentState == ParserStates.command_known_data_unknown:
            # Resolve argument types
            self.arg_reparse(textInput)
        else:
            print("No input required in: ", self.currentState)
