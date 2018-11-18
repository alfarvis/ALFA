#!/usr/bin/env python3
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern,
                                        findNumbers, searchDateTime)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
from Alfarvis.printers import Printer, TablePrinter
import pandas as pd
import numpy as np


class ConvertToDateTime(AbstractCommand):

    def briefDescription(self):
        return "convert array to date time month or year"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        return ["convert", "extract", "to date", "date time"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array),
                Argument(keyword="user_conv", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, array_data, user_conv):
        try:
            if isinstance(array_data.data[0], str):
                date_time = pd.to_datetime(
                    array_data.data, infer_datetime_format=True)
                array_data.data = date_time
            else:
                date_time = array_data.data
            if not isinstance(array_data.data[0], pd.datetime):
                raise RuntimeError()
        except:
            Printer.Print("Cannot transform data to date time")
            return ResultObject(None, None, None, CommandStatus.Error)
        results = []
        for word in ['day', 'year', 'month', 'hour', 'minute']:
            if word in user_conv.data or word + 's' in user_conv.data:
                out = getattr(date_time, word)
                result = ResultObject(out, [], DataType.array)
                result.createName(array_data.keyword_list, command_name=word,
                                  set_keyword_list=True)
                results.append(result)
                Printer.Print('Saving ', word, 'from ', array_data.name,
                              ' as', result.name)
        if results != []:
            return results
        return ResultObject(None, None, None, CommandStatus.Success)


class FilterTopN(AbstractCommand):
    """
    Create a filter with top N values
    """

    def briefDescription(self):
        return "find top N values in an array"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def __init__(self, condition=["top", "best", "largest"]):
        self._condition = condition

    def commandTags(self):
        """
        Tags to identify the condition
        """
        return self._condition + ["filter"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, array_data, target):
        result = ResultObject(None, None, None, CommandStatus.Error)
        in_array = array_data.data
        N = in_array.shape[0]
        if StatContainer.conditional_array is not None and len(StatContainer.conditional_array.data) == N:
            in_array = in_array[StatContainer.conditional_array.data]
        if in_array.size == 0:
            Printer.Print("No data")
            return result
        nan_idx = StatContainer.getNanIdx(in_array)
        non_nan_idx = np.logical_not(nan_idx)
        non_nan_array = in_array[non_nan_idx]
        numbers = findNumbers(target.data, 1)
        try:
            unique_arr, inv, counts = np.unique(
                non_nan_array, return_inverse=True, return_counts=True)
        except:
            return result
        if numbers != [] and numbers[0].data > 0:
            num = int(numbers[0].data)
            idx = None
            if not np.issubdtype(non_nan_array.dtype, np.number):
                num = min(unique_arr.size, num)
            if self._condition[0] == "top":
                Printer.Print("Finding top", num)
                if np.issubdtype(non_nan_array.dtype, np.number):
                    best_idx = np.argpartition(non_nan_array, -num)[-num:]
                    idx = np.full(non_nan_array.size, False)
                    idx[best_idx] = True
                    if num <= 30:
                        if StatContainer.row_labels is not None:
                            df_new = pd.DataFrame({array_data.name: non_nan_array[best_idx]})
                            df_new[StatContainer.row_labels.name] = StatContainer.row_labels.data[best_idx]
                            TablePrinter.printDataFrame(df_new)
                            TablePrinter.sort(0, ascending=False)
                        else:
                            Printer.Print("Top values:")
                            Printer.Print(non_nan_array[best_idx])
                else:
                    best_idx = np.argpartition(counts, -num)[-num:]
                    idx = np.isin(inv, best_idx)
                    if num <= 30:
                        Printer.Print("Top values:")
                        Printer.Print(unique_arr[best_idx])
            elif self._condition[0] == "bottom":
                Printer.Print("Finding bottom", num)
                if np.issubdtype(non_nan_array.dtype, np.number):
                    worst_idx = np.argpartition(non_nan_array, -num)[:num]
                    idx = np.full(non_nan_array.size, False)
                    idx[worst_idx] = True
                    if num <= 30:
                        if StatContainer.row_labels is not None:
                            df_new = pd.DataFrame({array_data.name: non_nan_array[worst_idx]})
                            df_new[StatContainer.row_labels.name] = StatContainer.row_labels.data[worst_idx]
                            TablePrinter.printDataFrame(df_new)
                            TablePrinter.sort(0, ascending=True)
                        else:
                            Printer.Print("Worst values:")
                            Printer.Print(non_nan_array[worst_idx])
                else:
                    worst_idx = np.argpartition(counts, num)[:num]
                    idx = np.isin(inv, worst_idx)
                    if num <= 30:
                        Printer.Print("Worst values:")
                        Printer.Print(unique_arr[worst_idx])
            elif self._condition[0] == "first":
                Printer.Print(array_data.data[:num])
                result = ResultObject(None, None, None, CommandStatus.Success)
            else:
                Printer.Print("Did not find the right condition")
            if idx is not None:
                out1 = np.full(in_array.size, False)
                out1[non_nan_idx] = idx
                if StatContainer.conditional_array is not None and len(StatContainer.conditional_array.data) == N:
                    out = np.full(N, False)
                    out[StatContainer.conditional_array.data] = out1
                else:
                    out = out1
                result = ResultObject(out, [], DataType.logical_array,
                                     CommandStatus.Success, True)
                result.createName(array_data.keyword_list,
                        command_name=self._condition[0],
                        set_keyword_list=True)
        elif self._condition[0] == "first":
            if unique_arr.size < 50:
                Printer.Print(unique_arr)
            else:
                Printer.Print(non_nan_array[:10])
            result = ResultObject(None, None, None, CommandStatus.Success)
        return result

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to filter?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to filter?")

class FilterBottomN(FilterTopN):

    def briefDescription(self):
        return "find bottom N values in an array"

    def __init__(self):
        super(FilterBottomN, self).__init__(["bottom", "worst", "smallest",
             "last"])


class FilterFirstN(FilterTopN):

    def briefDescription(self):
        return "print first N values of an array"

    def __init__(self):
        super(FilterFirstN, self).__init__(["first", "print"])


class LessThan(AbstractCommand):
    """
    create logical array with elements less than
    specified value
    """

    def briefDescription(self):
        return "find elements of an array less than target"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def __init__(self, condition=["less than", "smaller than", "before"],
                 operator='<'):
        self._condition = condition
        self._operator = operator

    def commandTags(self):
        """
        Tags to identify the condition
        """
        return self._condition + [self._operator, "conditional array",
                                  "logical array", "logic array", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, array_data, target):
        if (self._operator not in ['<', '<=', '>', '>='] or
            len(array_data.data) == 0):
            return ResultObject(None, None, None, CommandStatus.Error)
        date_times = searchDateTime(target.data)
        if all([indiv_list == [] for indiv_list in date_times]):
            numbers = findNumbers(target.data, 1)
            if numbers == []:
                return ResultObject(None, None, None, CommandStatus.Error)
            if isinstance(array_data.data[0], str):
                try:
                    date_time = pd.to_datetime(
                        array_data.data, infer_datetime_format=True)
                except:
                    print("Cannot convert ", array_data.name)
                    return ResultObject(None, None, None, CommandStatus.Error)
                array_data.data = date_time
                in_data = date_time.year
            elif isinstance(array_data.data[0], pd.datetime):
                in_data = array_data.data.year
            else:
                in_data = array_data.data
            return self.evaluateForNumbers(in_data, numbers[0],
                                           array_data.keyword_list)
        else:
            if isinstance(array_data.data[0], str):
                try:
                    in_data = pd.to_datetime(
                        array_data.data, infer_datetime_format=True)
                except:
                    print("Cannot convert ", array_data.name)
                    return ResultObject(None, None, None, CommandStatus.Error)
                array_data.data = in_data
            elif isinstance(array_data.data[0], pd.datetime):
                in_data = array_data.data
            else:
                Printer.Print("Array data type not understood for",
                              "comparing date time")
                return ResultObject(None, None, None, CommandStatus.Error)
            return self.evaluateForDateTime(in_data, date_times,
                                            array_data.keyword_list)
        return ResultObject(None, None, None, CommandStatus.Error)

    def performOperation(self, array1, array2):
        if self._operator == '<':
            return array1 < array2
        elif self._operator == '<=':
            return array1 <= array2
        elif self._operator == '>':
            return array1 > array2
        elif self._operator == '>=':
            return array1 >= array2

    def updateOutput(self, out, in_array, target, unresolved_idx):
        nan_idx = np.isnan(in_array)
        idx = np.logical_and(np.logical_not(nan_idx), unresolved_idx)
        op_out = self.performOperation(in_array[idx], target)
        unresolved_idx[nan_idx] = False
        unresolved_idx[idx] = (in_array[idx] == target)
        out[idx] = np.logical_and(out[idx], op_out)
        out[nan_idx] = False

    def createResult(self, out, keyword_list, create_name=True):
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
        if create_name:
            result.createName(keyword_list,
                              command_name=self._condition[0],
                              set_keyword_list=True)
        else:
            result.keyword_list = keyword_list
        return result

    def evaluateForDateTime(self, array_data, target_date_time_tup,
                            keyword_list, create_name=True):
        days, months, years, hours, minutes = target_date_time_tup
        out = np.full(array_data.shape, True)
        unresolved_idx = np.full(array_data.shape, True)
        if years != []:
            self.updateOutput(out, array_data.year, years[0], unresolved_idx)
        if months != [] and np.any(unresolved_idx):
            self.updateOutput(out, array_data.month, months[0], unresolved_idx)
        if days != [] and np.any(unresolved_idx):
            self.updateOutput(out, array_data.day, days[0], unresolved_idx)
        if hours != [] and np.any(unresolved_idx):
            self.updateOutput(out, array_data.hour, hours[0], unresolved_idx)
        if minutes != [] and np.any(unresolved_idx):
            self.updateOutput(out, array_data.minute, minutes[0],
                              unresolved_idx)
        if StatContainer.conditional_array is not None and len(StatContainer.conditional_array.data) == array_data.shape[0]:
            non_filt_idx = np.logical_not(StatContainer.conditional_array.data)
            out[non_filt_idx] = False
        return self.createResult(out, keyword_list, create_name)

    def evaluateForNumbers(self, array_data, target, keyword_list,
                           create_name=True):
        Printer.Print("Target: ", target.data)
        out = np.full(array_data.shape, True)
        unresolved_idx = np.full(array_data.shape, True)
        self.updateOutput(out, array_data, target.data, unresolved_idx)
        if StatContainer.conditional_array is not None:
            non_filt_idx = np.logical_not(StatContainer.conditional_array.data)
            out[non_filt_idx] = False
        return self.createResult(out, keyword_list, create_name)

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to filter?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to filter?")


class LessThanEqual(LessThan):

    def briefDescription(self):
        return "find elements of an array less than equal to target"

    def __init__(self):
        super(LessThanEqual, self).__init__(["equal", "less than",
                                             "smaller than", "before or"],
                                            '<=')


class GreaterThan(LessThan):

    def briefDescription(self):
        return "find elements of an array greater than target"

    def __init__(self):
        super(GreaterThan, self).__init__(["greater than", "bigger than",
                                           "after"], '>')


class GreaterThanEqual(LessThan):

    def briefDescription(self):
        return "find elements of an array greater than or equal to target"

    def __init__(self):
        super(GreaterThanEqual, self).__init__(
            ["equal",
             "after or", "greater than", "bigger than"], '>=')


# in between
class Between(AbstractCommand):
    """
    create logical array with elements between
    specified values
    """
    less_than = LessThan()
    greater_than = GreaterThan()

    def briefDescription(self):
        return "find elements of an array between targets"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        Tags to identify the condition
        TODO: Check if we can less and greater together?
        """
        return ["between", "in between",
                "inside", "inside range",
                "in range", "conditional array",
                "logical array", "logic array", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def createResult(self, out, keyword_list):
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
        result.createName(keyword_list, command_name='between',
                          set_keyword_list=True)
        return result

    def evaluate(self, array_data, target):
        if len(array_data.data) == 0:
            return ResultObject(None, None, None, CommandStatus.Error)
        date_times = searchDateTime(target.data)
        if all([indiv_list == [] for indiv_list in date_times]):
            numbers = findNumbers(target.data, 2)
            if len(numbers) < 2:
                Printer.Print("Cannot find enough numbers. Please provide two numbers")
                return ResultObject(None, None, None, CommandStatus.Error)
            if isinstance(array_data.data[0], str):
                try:
                    date_time = pd.to_datetime(
                        array_data.data, infer_datetime_format=True)
                except:
                    print("Cannot convert ", array_data.name)
                    return ResultObject(None, None, None, CommandStatus.Error)
                array_data.data = date_time
                in_data = date_time.year
            else:
                in_data = array_data.data
            out1 = self.less_than.evaluateForNumbers(in_data, numbers[1],
                                                   array_data.keyword_list,
                                                   create_name=False)
            out2 = self.greater_than.evaluateForNumbers(in_data, numbers[0],
                                                      array_data.keyword_list,
                                                      create_name=False)
            out = np.logical_and(out1.data, out2.data)
            return self.createResult(out, array_data.keyword_list)
        else:
            if isinstance(array_data.data[0], str):
                try:
                    in_data = pd.to_datetime(array_data.data,
                                             infer_datetime_format=True)
                except:
                    print("Cannot convert ", array_data.name)
                    return ResultObject(None, None, None, CommandStatus.Error)
                array_data.data = in_data
            elif isinstance(array_data.data[0], pd.datetime):
                in_data = array_data.data
            else:
                Printer.Print("Array data type not understood for comparing date time")
                return ResultObject(None, None, None, CommandStatus.Error)
            # Expand date_times
            date_time_list1 = []
            date_time_list2 = []
            for indiv_list in date_times:
                if len(indiv_list) == 0:
                    date_time_list1.append([])
                    date_time_list2.append([])
                if len(indiv_list) == 1:
                    date_time_list1.append([indiv_list[0]])
                    date_time_list2.append([indiv_list[0]])
                elif len(indiv_list) > 1:
                    date_time_list1.append([indiv_list[0]])
                    date_time_list2.append([indiv_list[1]])
            out1 = self.greater_than.evaluateForDateTime(
                    in_data, date_time_list1, array_data.keyword_list,
                    create_name=False)
            out2 = self.less_than.evaluateForDateTime(
                    in_data, date_time_list2, array_data.keyword_list,
                    create_name=False)
            out = np.logical_and(out1.data, out2.data)
            return self.createResult(out, array_data.keyword_list)
        return ResultObject(None, None, None, CommandStatus.Error)

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to filter?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to filter?")


class Outside(AbstractCommand):
    """
    create logical array with elements outside
    specified values
    """
    between = Between()

    def briefDescription(self):
        return "find elements of an array outside specified targets"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        Tags to identify the condition
        TODO: Check if we can less and greater together?
        """
        return ["outside", "not in",
                "outside range", "conditional array",
                "logical array", "logic array", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, array_data, target):
        result = self.between.evaluate(array_data, target)
        result.removeName(result.name)
        result.data = np.logical_not(result.data)
        result.createName(array_data.keyword_list, command_name='outside',
                          set_keyword_list=True)
        return result

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to filter?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to filter?")


class Contains(AbstractCommand):
    """
    create logical array with elements containing specified text
    """

    def briefDescription(self):
        return "find elements of an array containing specified string"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def commandTags(self):
        """
        Tags to identify the command
        """
        return ["contains", "conditional array",
                "logical array", "logic array", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         tags=[Argument.Tag('contains',
                                            Argument.TagPosition.After),
                               Argument.Tag('has',
                                            Argument.TagPosition.After)],
                         argument_type=DataType.user_string)]

    def containsWordList(self, target, word_list):
        if isinstance(target, str):
            target_lower = target.lower()
            for word in word_list:
                if word in target_lower:
                    return True
        return False

    def evaluate(self, array_data, target):
        split_target = splitPattern(target.data)
        out = np.array([self.containsWordList(
            data, split_target) for data in array_data.data])
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
        result.createName(array_data.keyword_list, split_target,
                          command_name='contains', set_keyword_list=True)
        return result

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to filter?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to filter?")

# Combine conditions


class LogicalAnd(AbstractCommand):
    """
    combine two logical arrays
    """

    def briefDescription(self):
        return "find logical and among arrays"

    def commandType(self):
        return AbstractCommand.CommandType.DataHandling

    def __init__(self, add_tags=["and"], operator='&'):
        self._add_tags = add_tags
        self._operator = operator

    def commandTags(self):
        """
        Tags to identify the condition
        """
        tags = []
        for tag in self._add_tags:
            tags.append("logic " + tag)
            tags.append("logical " + tag)
        tags.append(self._operator)
        tags = tags + ["conditional array", "create"]
        return tags

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=False,
                argument_type=DataType.logical_array, number=-1)]

    def evaluate(self, array_data):
        N = len(array_data)
        if N < 1:
            return ResultObject(None, None, None, CommandStatus.Error)
        out = array_data[0].data
        Printer.Print("Performing logical", self._add_tags[0], "on ")
        Printer.Print(array_data[0].name)
        if self._operator == '!':
            out = np.logical_not(array_data[0].data)

        for arr_data in array_data[1:]:
            Printer.Print(", ", arr_data.name)
            if self._operator == '&':
                out = np.logical_and(out, arr_data.data)
            elif self._operator == '||':
                out = np.logical_or(out, arr_data.data)
            elif self._operator == '^':
                out = np.logical_xor(out, arr_data.data)
            else:
                return ResultObject(None, None, None, CommandStatus.Error)
            Printer.Print(arr_data.name)
        if StatContainer.conditional_array is not None:
            non_filt_idx = np.logical_not(StatContainer.conditional_array)
            out[non_filt_idx] = False
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
        if len(array_data) > 1:
            keyword_list2 = array_data[1].keyword_list
        else:
            keyword_list2 = []
        result.createName(array_data[0].keyword_list, keyword_list2,
                          command_name=self._add_tags[0],
                          set_keyword_list=True)
        return result

    def ArgNotFoundResponse(self,array_datas):
        Printer.Print("Which variable do you want me to filter?")
    
    def ArgFoundResponse(self,array_datas):
        Printer.Print("Found variables") # will only be called for commands with multiple arg types
        
    def MultipleArgsFoundResponse(self, array_datas):
        Printer.Print("I found multiple variables that seem to match your query")
        Printer.Print("Could you please look at the following variables and tell me which one you "
              "want to filter?")


class LogicalOr(LogicalAnd):

    def briefDescription(self):
        return "find logical or among arrays"

    def __init__(self):
        super(LogicalOr, self).__init__(["or"], '||')


class LogicalNot(LogicalAnd):

    def briefDescription(self):
        return "find logical not between arrays"

    def __init__(self):
        super(LogicalNot, self).__init__(["not"], '!')


class LogicalXor(LogicalAnd):

    def briefDescription(self):
        return "find logical xor among arrays"

    def __init__(self):
        super(LogicalXor, self).__init__(["xor"], '^')
