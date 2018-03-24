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
                    self.printCommands(self.command_search_result)
            else:
                self.command_search_result = res
                self.printCommands(self.command_search_result)
    
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
        if 'quit' in split_text:
            self.clearCommandSearchResults()
        else:
            self.resolveArguments(split_text)

    def resolveArguments(self, key_words):
        all_arg_names = set()
        for i in range (len(self.argumentTypes)):
            # TODO Try to use information from user when command gives error
            # TODO If user wants to substitute arguments in the process of resolution then ask him for confirmation. 
            arg_type = self.argumentTypes[i].argument_type
            arg_name = self.argumentTypes[i].keyword
            if arg_name in self.argumentsFound:
                continue
            data_res = self.history.search(arg_type, key_words)
            all_arg_names.add(arg_name)
            if len(data_res)==1:
                self.argumentsFound[arg_name] = data_res[0].data
            elif len(data_res) > 1:
                if arg_name in self.argument_search_result:
                    intersection_set = self.findIntersection(self.argument_search_result[arg_name],
                                                             data_res)
                    if len(intersection_set) == 0:
                        self.argument_search_result[arg_name] = data_res
                    elif len(intersection_set) == 1:
                        self.argumentsFound[arg_name] = intersection_set.pop().data
                    else:
                        self.argument_search_result[arg_name] = list(intersection_set)
                else:
                    self.argument_search_result[arg_name] = data_res
        if len(self.argumentTypes) == len(self.argumentsFound):
            self.currentState = ParserStates.command_known_data_known
            self.argument_search_result = {}
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
            # TODO Find which arguments are wrong and resolve only those data
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


