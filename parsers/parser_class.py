from parser_states import ParserStates
from Alfarvis import create_command_database
from Alfarvis.basic_definitions import CommandStatus


class AlfaDataParser:
    def __init__(self, history):
        self.textInput = ""
        self.history = history # Data history
        self.command_database = create_command_database(history) # Command database
        self.clearCommandSearchResults()

    def clearCommandSearchResults(self):
        """
        Clear keyword list and command search result
        """
        self.currentState = ParserStates.command_unknown  # Parser state
        self.keyword_list = []  # Keywords extracted from input text
        self.command_search_result = []  # If a command is currently being parsed, resolve arguments for that command
        self.argumentsFound = {}  # Resolved arguments to separate from unresolved args
        self.argument_search_result = {} # To resolve argument search results
    
    def findIntersection(self, list1, list2):
        return set(list1).intersection(set(list2))

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
            res = self.command_database.search(split_text)
        else:
            # Tokenize text
            self.keyword_list.append(split_text)
            res = self.command_database.search(self.keyword_list)
        if len(res) == 0:
            print("Command not found")
            print("If you would like to know about existing commands, please say Find commands or Please help me")
            self.clearCommandSearchResults()
        elif len(res) == 1:
            self.foundCommand(res)
        else:
            if len(self.command_search_result) > 0:
                intersection_set = self.findIntersection(self.command_search_result, res)
                if len(intersection_set) == 0:
                    self.command_search_result = res
                    print("The new commands do not match with the old input.")
                elif len(intersection_set) == 1:
                    self.foundCommand(list(intersection_set))
                else:
                    self.command_search_result = list(intersection_set)
                    print("Found multiple commands. Please select one of the commands")
            else:
                self.command_search_result = res
                print("Found multiple commands. Please select one of the commands")
    
    def foundCommand(self, res):
        print("Found command", res[0])
        self.currentState = ParserStates.command_known
        self.currentCommand = res[0].data
        self.argumentTypes = self.currentCommand.argumentTypes()
        self.resolveArguments(self.keyword_list)

    def data_parse(self, text):
        # Tokenize text
        # Resolve arguments or data
        split_text = text.split(" ")
        # TODO Get out of the resolve args if user wants to
        # Tokenize text
        self.resolveArguments(split_text)
        return 0

    def resolveArguments(self, key_words):
        all_arg_names = set()
        for i in range (len(self.argumentTypes)):
            # TODO Only resolve args which are not foundfff
            # TODO Try to use information from user when command gives error
            arg_type = self.argumentTypes[i].argument_type
            arg_name = self.argumentTypes[i].keyword
            data_res = self.history.search(arg_type, key_words)
            all_arg_names.add(arg_name)
            if len(data_res==1):
                self.argumentsFound[arg_name] = data_res[0].data
            elif len(data_res > 1):
                if arg_name in self.argument_search_results:
                    intersection_set = self.findIntersection(self.argument_search_result[arg_name],
                                                             data_res)
                    if len(intersection_set) == 0:
                        self.argument_search_result[arg_name] = data_res
                    elif len(intersection_set) == 1:
                        intersection_list = list(intersection_set)
                        self.argumentsFound[arg_name] = intersection_list[0].data
                    else:
                        self.argument_search_result[arg_name] = list(intersection_set)
                else:
                    self.argument_search_result[arg_name] = data_res
        if len(self.argumentTypes) == len(self.argumentsFound):
            self.currentState = ParserStates.command_known_data_known
            self.executeCommand(self.command, self.argumentsFound)
        else:
            self.currentState = ParserStates.command_known_data_unknown
            unknown_args = all_arg_names.difference(set(self.argumentsFound.keys()))
            # Get a list of unknown arguments"
            print("Cannot find some arguments", unknown_args)

    def executeCommand(self, command, arguments):
        # Execute command and take action based on result
        command_status = command.evaluate(**arguments)
        if command_status == CommandStatus.Error:
            self.currentState = ParserStates.command_known_data_unknown
        elif command_status == CommandStatus.Success:
            self.currentState = ParserStates.command_unknown
            self.clearCommandSearchResults()
        return 0
        
    def parse(self,textInput):
        """
        Take input from user and resolve/run the instructions
        """
        # Tokenizer and create keyword list
        if self.currentState == ParserStates.command_unknown:
            self.command_parse(textInput)
        elif self.currentState == ParserStates.command_known_data_unknown:
            # Resolve argument types
            self.data_parse(textInput)
        else:
            print("No input required in: ", self.currentState)

    def getCurrentState(self):
        return self.currentState

    def FindArgumentFromHistory(self):
        return 0 


