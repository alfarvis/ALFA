from .parser_states import ParserStates
from Alfarvis.commands import create_command_database
from Alfarvis.commands.argument import Argument
from Alfarvis.history import TypeDatabase
from Alfarvis.basic_definitions import CommandStatus, DataType, DataObject
import numpy as np

# TODO Remove/split based on commas and semicolumns etc
# TODO Handle capitalization when user string input is used


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
        # Resolved arguments to separate from unresolved args
        self.argumentsFound = {}
        self.argument_search_result = {}  # To resolve argument search results

    @classmethod
    def findIntersection(self, list1, list2):
        return set(list1).intersection(set(list2))

    @classmethod
    def findUnion(self, list1, list2):
        return set(list1).union(set(list2))

    def printCommands(self, command_list):
        print("Found multiple commands. Please select one of the commands")
        for command in command_list:
            print(command.keyword_list[0])

    # Keeping it different for commands and arguments for now in case we want
    # to add further intelligence in either which might have a different logic
    def printArguments(self, args):

        for arg in args:
            print(" ".join(arg.keyword_list))

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
            print("If you would like to know about existing commands,"
                  " please say Find commands or Please help me")
            self.clearCommandSearchResults()
        elif len(res) == 1:
            self.foundCommand(res[0])
        else:
            closest_match = self.findClosestMatch(res)
            if closest_match is not None:
                self.foundCommand(closest_match)
            elif len(self.command_search_result) > 0:
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

    @classmethod
    def getMinIndices(self, array):
        """
        Find the indices of all the elements that have the smallest value in
        the array
        Parameters:
            array - Any iterable with elements that can be compared to a
                    numeric value
        Return: the indices of the minimum values in the array
        """
        out = []
        min_val = np.Inf
        for i, val in enumerate(array):
            if val < min_val:
                min_val = val
                out = [i]
            elif val == min_val:
                out.append(i)
        return out

    def findClosestMatch(self, match_res):
        data_len_list = [data.length for data in match_res]
        idx = self.getMinIndices(data_len_list)
        if len(idx) == 1:
            return match_res[idx[0]]
        return None

    def fillClosestArguments(self, argument_search_result,
                             argumentsFound, argumentTypes):
        """
        If an argument has multiple hits, find the closest one based on
        percent match in the target match. For example
        "favorite quote" matches with
        ("favorite quote", "favorite quote length"). If both elements
        have same type, then we want to choose "favorite quote" which has
        100% percent match.
        Parameters:
            argument_search_result - dictionary with multiple data results
            argumentsFound - arguments that have already been found
            argumentTypes - list of arguments accepted by the command
        Return:
            Fill arguments found
        """
        for argument in argumentTypes:
            arg_name = argument.keyword
            arg_number = argument.number
            # Currently we only handle closest match of single sized arguments
            if (arg_name in argument_search_result and
                    arg_number == 1):
                match_res = argument_search_result[arg_name]
                closest_match = self.findClosestMatch(match_res)
                if closest_match is not None:
                    argumentsFound[arg_name] = closest_match

    def fillOptionalArguments(self, argumentsFound, argumentTypes):
        """
        Fill optional arguments with last object from cache
        """
        for argument in argumentTypes:
            arg_types = self.wrap(argument.argument_type)
            arg_name = argument.keyword
            arg_number = argument.number
            if (argument.optional and
                (arg_name not in argumentsFound) and
                    (arg_name not in self.argument_search_result)):
                if not argument.fill_from_cache:
                    argumentsFound[arg_name] = None
                    continue
                if arg_number > 1:
                    print("Arguments with multi-input cannot be optional")
                    continue
                cache_res = self.history.getLastObject(arg_types[0])
                if cache_res is not None:
                    # Use unwrap for infinite args
                    argumentsFound[arg_name] = cache_res

    def checkArgumentsFound(self, argumentsFound, argumentTypes):
        """
        Check all non optional arguments are found
        """
        for argument in argumentTypes:
            if argument.keyword not in argumentsFound:
                return False
        return True

    @classmethod
    def unwrap(self, in_list, arg_number):
        """
        If the list size is one, it unwraps the list
        and returns the actual value
        """
        if len(in_list) == 1 and arg_number == 1:
            return in_list[0]
        return in_list

    @classmethod
    def wrap(self, in_object):
        """
        If input object is a single data type wraps
        it into a list
        """
        if type(in_object) == DataType:
            return [in_object]
        return in_object

    def checkArgumentNumber(self, argument_number, data_res_len):
        """
        Check argument number matches with number of arguments
        found for that argument type
        """
        return ((argument_number == -1 and data_res_len > 0) or
                (data_res_len == argument_number))

    @classmethod
    def get_number(self, string_in):
        """
        Convert string to number if possible.
        """
        try:
            res = float(string_in)
        except:
            res = None
        return res

    @classmethod
    def findNumbers(self, keyword_list, N):
        """
        Find numbers from given keyword list. Will search for N
        arguments
        """
        data_res = []
        for keyword in keyword_list:
            res = self.get_number(keyword)
            if res is not None:
                data_res.append(DataObject(res, []))
            if len(data_res) == N:
                break
        return data_res

    @classmethod
    def extractArgFromUser(self, key_words, argument):
        """
        Extract argument from user input if possible
        """
        data_res = []
        for tag in argument.tags:
            try:
                index = key_words.index(tag.name)
            except:
                continue

            if tag.position == Argument.TagPosition.After:
                search_scope = key_words[(index + 1):]
            elif tag.position == Argument.TagPosition.Before:
                # Reverse list to be consistent with search
                # order
                search_scope = key_words[:index][::-1]
            else:
                search_scope = key_words

            if argument.argument_type is DataType.number:
                res = self.findNumbers(search_scope,
                                       argument.number)
                if len(res) != 0:
                    data_res = data_res + res
                    break
            elif argument.argument_type is DataType.user_string:
                res = DataObject(' '.join(search_scope), search_scope)
                data_res.append(res)
                break
            else:
                print("Can only extract numbers and strings from user"
                      "currently")
                break
        return data_res

    def searchHistory(self, argument, key_words):
        """
        Go through arg types and try to find the requested number from
        history.
        """
        arg_types = self.wrap(argument.argument_type)
        hit_count = 0
        data_res = []
        for arg_type in arg_types:
            # If argument is supposed to be extracted from user
            # as opposed to from history
            if (arg_type is DataType.number or
                    arg_type is DataType.user_string):
                current_res = self.extractArgFromUser(key_words, argument)
                if len(current_res) != 0:
                    data_res = current_res
                    break
            else:
                current_res = self.history.search(arg_type, key_words)
                current_hits = self.history.getHitCount(arg_type)
                if (len(current_res) >= argument.number and
                        current_hits > hit_count):
                    data_res = current_res
                    hit_count = current_hits
            # In the beginning add current res to make sure we have something
            if hit_count == 0:
                data_res = current_res
        return data_res

    def resolveArguments(self, key_words):
        all_arg_names = set()
        argumentTypes = self.currentCommand.argumentTypes()
        for argument in argumentTypes:
            # TODO Try to use information from user when command gives error
            # TODO If user wants to substitute arguments in the process of
            # resolution then ask him for confirmation.
            # TODO Handle composite commands (resolveCommands similar to
            # resolveArguments)
            assert(argument.number != 0)
            arg_type = argument.argument_type
            arg_name = argument.keyword
            if arg_name in self.argumentsFound:
                continue
            if arg_type is DataType.user_conversation:
                self.argumentsFound[arg_name] = DataObject(
                    key_words, ['user', 'coversation'])
                continue
            elif arg_type is DataType.history:
                self.argumentsFound[arg_name] = DataObject(self.history,
                                                           ['history'])
                continue
            data_res = self.searchHistory(argument, key_words)
            all_arg_names.add(arg_name)
            # If infinite args allowed and we found some args or
            # if finite args allowed and we found exactly those
            # many arguments
            # TODO print intelligent responses as in which arguments
            # are missing or more?
            if self.checkArgumentNumber(argument.number, len(data_res)):
                self.argumentsFound[arg_name] = self.unwrap(data_res,
                                                            argument.number)
            elif len(data_res) != argument.number and len(data_res) > 0:
                if arg_name in self.argument_search_result:
                    previous_result = self.argument_search_result[arg_name]
                    if len(previous_result) > argument.number:
                        res_set = self.findIntersection(
                            previous_result, data_res)
                    else:
                        res_set = self.findUnion(previous_result, data_res)
                    if len(res_set) == argument.number:
                        self.argumentsFound[arg_name] = self.unwrap(
                            list(res_set), argument.number)
                    elif len(res_set) == 0:
                        self.argument_search_result[arg_name] = data_res
                    else:
                        self.argument_search_result[
                            arg_name] = list(res_set)

                else:
                    self.argument_search_result[arg_name] = data_res
        self.fillClosestArguments(self.argument_search_result,
                                  self.argumentsFound,
                                  argumentTypes)
        # Fill all the optional arguments
        self.fillOptionalArguments(self.argumentsFound, argumentTypes)
        if self.checkArgumentsFound(self.argumentsFound, argumentTypes):
            self.currentState = ParserStates.command_known_data_known
            self.argument_search_result = {}
            self.executeCommand(self.currentCommand, self.argumentsFound)
        else:
            self.currentState = ParserStates.command_known_data_unknown
            unknown_args = all_arg_names.difference(
                set(self.argumentsFound.keys()))
            # Get a list of unknown arguments"
            print("\nChecking for arguments...\n")
            unknownList = list(unknown_args)
            for arg in self.argumentsFound:
                print("Argument ", arg, "found")
                print("Matching argument: ",
                      self.printArguments([self.argumentsFound[arg]]))
            for arg in unknown_args:
                if arg in self.argument_search_result:
                    print("\nMultiple arguments found for ", arg)
                    (self.printArguments(
                        self.argument_search_result[arg]))
                else:
                    print("Could not find any match for ", arg)
            if len(unknownList) > 0:
                print("\nPlease provide more clues to help me resolve",
                      "these arguments")

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
            print("\nFailed to execute command")
            print("Please provide new arguments or "
                  "Type Quit to change your command")
            # TODO Find which arguments are wrong and resolve only those data
        elif (result.command_status == CommandStatus.Success):
            # TODO Add a new function to add result to history
            if (result.data_type is not None):
                self.history.add(result.data_type, result.keyword_list,
                                 result.data, result.add_to_cache, result.name)
            self.currentState = ParserStates.command_unknown
            self.clearCommandSearchResults()

    def parse(self, textInput):
        """
        Take input from user and resolve/run the instructions
        """
        textInput = textInput.lower()
        # Tokenizer and create keyword list
        if self.currentState == ParserStates.command_unknown:
            self.command_parse(textInput)
        elif self.currentState == ParserStates.command_known_data_unknown:
            # Resolve argument types
            self.arg_reparse(textInput)
        else:
            print("No input required in: ", self.currentState)
