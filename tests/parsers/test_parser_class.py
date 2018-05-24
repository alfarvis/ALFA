#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 22:34:24 2018

@author: vishwaparekh
"""

import unittest
from Alfarvis.parsers import AlfaDataParser, ParserStates
from Alfarvis.basic_definitions import (DataObject, DataType, ResultObject)
from Alfarvis.commands.abstract_command import AbstractCommand
from Alfarvis.commands.argument import Argument


class DummyCommand(AbstractCommand):

    def commandTags(self):
        return ["dummy", "test"]

    def argumentTypes(self):
        return [Argument(keyword="dummy", optional=False,
                         argument_type=DataType.string)]

    def evaluate(self, dummy):
        return ResultObject(dummy.data, ["dummy", "result"], DataType.string)


class CommandWithMultiArgNumber(AbstractCommand):

    def commandTags(self):
        return ["multi", "arg", "fun"]

    def argumentTypes(self):
        return [Argument(keyword="dummy", optional=False,
                         argument_type=DataType.string,
                         number=4)]

    def evaluate(self, dummy):
        result_data = set()
        for i in range(4):
            result_data.add(dummy[i].data)
        return ResultObject(result_data, ["dummy", "result"], DataType.string)


class CommandWithInfArgNumber(AbstractCommand):

    def commandTags(self):
        return ["inf", "arg", "fun"]

    def argumentTypes(self):
        return [Argument(keyword="dummy", optional=False,
                         argument_type=DataType.string,
                         number=-1)]

    def evaluate(self, dummy):
        result_data = set()
        for dummy_in in dummy:
            result_data.add(dummy_in.data)
        return ResultObject(result_data, ["dummy", "result"], DataType.string)


class TestParserMethods(unittest.
                        TestCase):

    def setUp(self):
        self.parser = AlfaDataParser()
        self.history = self.parser.history

    def checkResult(self, history, expected_result, keywords, data_type):
        res = self.history.search(DataType.string, keywords)
        if len(res) != 1:
            print("Multiple entries found")
            return False
        data_obj = res[0]
        return (data_obj.data == expected_result)

    def test_find_intersection(self):
        self.assertEqual(AlfaDataParser.findIntersection(
            [1, 2, 3], [4, 3, 5]), {3})

    def test_find_union(self):
        self.assertEqual(AlfaDataParser.findUnion(
            [1, 2, 3], [4, 3, 5]), {1, 2, 3, 4, 5})

    def test_print_commands(self):
        command_list = [DataObject(None, ['load']),
                        DataObject(None, ['Random Forrest'])]
        self.parser.printCommands(command_list)

    def test_fill_optional_arguments(self):
        # Set up a few dummy arguments
        argumentTypes = [Argument(keyword="dummy1", optional=True,
                                  argument_type=DataType.string),
                         Argument(keyword="dummy2", optional=False,
                                  argument_type=DataType.string)]
        self.history.add(DataType.string, ["input", "my"], "dummy input")
        data_object = self.history.search(DataType.string, ["my", "input"])[0]
        argumentsFound = {}
        self.parser.fillOptionalArguments(argumentsFound, argumentTypes)
        self.assertTrue('dummy1' in argumentsFound)
        self.assertFalse('dummy2' in argumentsFound)
        self.assertEqual(argumentsFound['dummy1'], data_object)

    def test_fill_optional_arguments_already_found(self):
        # Set up a few dummy arguments
        argumentTypes = [Argument(keyword="dummy1", optional=True,
                                  argument_type=DataType.string),
                         Argument(keyword="dummy2", optional=False,
                                  argument_type=DataType.string)]
        self.history.add(DataType.string, ["input", "my"], "dummy input")
        data_object = self.history.search(DataType.string, ["my", "input"])[0]
        argumentsFound = {'dummy1': 'Found'}
        self.parser.fillOptionalArguments(argumentsFound, argumentTypes)
        self.assertTrue('dummy1' in argumentsFound)
        self.assertFalse('dummy2' in argumentsFound)
        self.assertEqual(argumentsFound['dummy1'], 'Found')

    def test_execute_command(self):
        command = DummyCommand()
        dummy_input = DataObject("How are you", ["question"])
        self.parser.executeCommand(command, {"dummy": dummy_input})
        out = self.checkResult(self.history, "How are you", ["dummy"],
                               DataType.string)
        self.assertTrue(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_resolve_argument(self):
        self.history.add(DataType.string, ["input", "my"], "dummy input")
        self.history.add(DataType.string, ["quote", "favorite"],
                         "Pen is sharper than knife")
        key_words = "Call the dummy function with my input".split(' ')
        self.parser.currentCommand = DummyCommand()
        self.parser.resolveArguments(key_words)
        out = self.checkResult(self.history, "dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_resolve_argument_multi_arg_number(self):
        for i in range(4):
            input_val = "input" + str(i + 1)
            self.history.add(DataType.string, [input_val], input_val)
        key_words = ("Call the multi arg function with input1 input2"
                     " input3 input4").split(' ')
        self.parser.currentCommand = CommandWithMultiArgNumber()
        self.parser.resolveArguments(key_words)
        out = self.checkResult(self.history,
                               {"input1", "input2", "input3", "input4"},
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_resolve_argument_inf_arg_number(self):
        for i in range(10):
            input_val = "input" + str(i + 1)
            self.history.add(DataType.string, [input_val], input_val)
        key_words = ("Call the inf arg function with input1 input2"
                     " input7").split(' ')
        self.parser.currentCommand = CommandWithInfArgNumber()
        self.parser.resolveArguments(key_words)
        out = self.checkResult(self.history,
                               {"input1", "input2", "input7"},
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_overspecify_resolve_argument_multi_arg_number(self):
        for i in range(6):
            input_val = "input" + str(i + 1)
            self.history.add(DataType.string, [input_val], input_val)
        key_words = ("Call the multi arg function with input1 input2"
                     " input3 input4 input5 input6").split(' ')
        self.parser.currentCommand = CommandWithMultiArgNumber()
        self.parser.resolveArguments(key_words)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_known_data_unknown)
        # Try resolving now
        key_words = "Use input5 input2 input3 input4".split(' ')
        self.parser.resolveArguments(key_words)
        out = self.checkResult(self.history,
                               {"input2", "input3", "input4", "input5"},
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_underspecify_resolve_argument_multi_arg_number(self):
        for i in range(6):
            input_val = "input" + str(i + 1)
            self.history.add(DataType.string, [input_val], input_val)
        key_words = "Call the multi arg function with input1 input2".split(' ')
        self.parser.currentCommand = CommandWithMultiArgNumber()
        self.parser.resolveArguments(key_words)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_known_data_unknown)
        # Try resolving now
        key_words = "Also use input3 input5".split(' ')
        self.parser.resolveArguments(key_words)
        out = self.checkResult(self.history,
                               {"input3", "input2", "input5", "input1"},
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_unsuccessful_resolve_argument(self):
        self.history.add(DataType.string, ["quote", "favorite"],
                         "Pen is sharper than knife")

        key_words = "Call the dummy function with my input".split(' ')
        self.parser.currentCommand = DummyCommand()
        self.parser.resolveArguments(key_words)
        out = self.checkResult(self.history, "Pen is sharper than knife",
                               ["dummy", "result"], DataType.string)
        self.assertFalse(out)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_known_data_unknown)

    def test_unsuccessful_resolve_argument_multiple_results(self):
        self.history.add(DataType.string, ["quote", "favorite"],
                         "Pen is sharper than knife")
        self.history.add(DataType.string, ["pen", "favorite"],
                         "Reynolds")
        self.history.add(DataType.string, ["quote", "hate"],
                         "Pen is not sharper than knife")
        key_words = "Call the dummy function with my quote".split(' ')
        self.parser.currentCommand = DummyCommand()
        self.parser.resolveArguments(key_words)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_known_data_unknown)
        # Resolve arguments
        key_words = "favorite one".split(' ')
        self.parser.resolveArguments(key_words)
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)
        out = self.checkResult(self.history, "Pen is sharper than knife",
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)

    def test_arg_reparse_quit(self):
        self.parser.currentState = ParserStates.command_known_data_unknown
        self.parser.arg_reparse('please quit')
        self.assertEqual(self.parser.currentState,
                         ParserStates.command_unknown)

    def test_arg_reparse(self):
        self.history.add(DataType.string, ["input", "my"], "my dummy input")
        self.history.add(DataType.string, [
                         "input", "your"], "your dummy input")
        self.parser.state = ParserStates.command_known_data_unknown
        self.parser.currentCommand = DummyCommand()
        res = self.history.search(DataType.string, "input")
        # Set multiple results to parse from
        self.parser.argument_search_result["dummy"] = res
        self.parser.arg_reparse("Use my input")
        out = self.checkResult(self.history, "my dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        out = self.checkResult(self.history, "your dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertFalse(out)

    def test_found_command(self):
        self.history.add(DataType.string, ["input", "my"], "my dummy input")
        self.history.add(DataType.string, [
                         "input", "your"], "your dummy input")
        input_text = "Call the dummy function with my input"
        self.parser.keyword_list = input_text.split(' ')
        cmd_in = DataObject(DummyCommand(), ["dummy", "test"])
        self.parser.foundCommand(cmd_in)

        out = self.checkResult(self.history, "my dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)
        out = self.checkResult(self.history, "your dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertFalse(out)

    def test_command_parse(self):
        self.history.add(DataType.string, ["input", "my"], "my dummy input")
        self.history.add(DataType.string, [
                         "input", "your"], "your dummy input")
        self.parser.command_parse("Call the dummy function with your input")
        out = self.checkResult(self.history, "my dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertFalse(out)
        out = self.checkResult(self.history, "your dummy input",
                               ["dummy", "result"], DataType.string)
        self.assertTrue(out)

if __name__ == '__main__':
    unittest.main()
