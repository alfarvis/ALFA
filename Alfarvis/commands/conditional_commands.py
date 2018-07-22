#!/usr/bin/env python3
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern,
                                        findNumbers, searchDateTime)
from .abstract_command import AbstractCommand
from .argument import Argument
import pandas as pd
import numpy as np


class ConvertToDateTime(AbstractCommand):

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
            print("Cannot transform data to date time")
            return ResultObject(None, None, None, CommandStatus.Error)
        results = []
        for word in ['day', 'year', 'month', 'hour', 'minute']:
            if word in user_conv.data or word + 's' in user_conv.data:
                out = getattr(date_time, word)
                result = ResultObject(out, [], DataType.array)
                result.createName(array_data.keyword_list, command_name=word,
                                  set_keyword_list=True)
                results.append(result)
                print('Saving ', word, 'from ', array_data.name,
                      ' as', result.name)
        if results != []:
            return results
        return ResultObject(None, None, None, CommandStatus.Success)


class FilterTopN(AbstractCommand):
    """
    Create a filter with top N values
    """

    def __init__(self, condition=["top", "best", "largest"]):
        self._condition = condition

    def commandTags(self):
        """
        Tags to identify the condition
        """
        return self._condition + ["create filter"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                         argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, array_data, target):
        result = ResultObject(None, None, None, CommandStatus.Error)
        in_array = array_data.data
        N = in_array.shape[0]
        if in_array.size == 0:
            print("No data")
            return result
        if isinstance(array_data.data[0], pd.datetime):
            nan_idx = np.isnat(in_array)
        elif np.issubdtype(in_array.dtype, np.number):
            nan_idx = np.isnan(in_array)
        else:
            nan_idx = np.full(N, False)
        non_nan_idx = np.logical_not(nan_idx)
        non_nan_array = in_array[non_nan_idx]
        numbers = findNumbers(target.data, 1)
        if numbers != [] and numbers[0].data > 0:
            num = int(numbers[0].data)
            idx = None
            unique_arr, inv, counts = np.unique(
                non_nan_array, return_inverse=True, return_counts=True)
            if self._condition[0] == "top":
                print("Finding top", num)
                best_idx = np.argpartition(counts, -num)[-num:]
                idx = np.isin(inv, best_idx)
                if num <= 10:
                    print("Top values:")
                    print(unique_arr[best_idx])
            elif self._condition[0] == "bottom":
                print("Finding bottom", num)
                worst_idx = np.argpartition(counts, num)[:num]
                idx = np.isin(inv, worst_idx)
                if num <= 10:
                    print("Worst values:")
                    print(unique_arr[worst_idx])
            else:
                print("Did not find the right condition")
            if idx is not None:
                out = np.full(N, False)
                out[non_nan_idx] = idx
                result = ResultObject(out, [], DataType.logical_array,
                                     CommandStatus.Success, True)
                result.createName(array_data.keyword_list,
                        command_name=self._condition[0],
                        set_keyword_list=True)
        return result


class FilterBottomN(FilterTopN):
    def __init__(self):
        super(FilterBottomN, self).__init__(["bottom", "worst", "smallest",
             "last"])


class LessThan(AbstractCommand):
    """
    create logical array with elements less than
    specified value
    """

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
                date_time = pd.to_datetime(
                    array_data.data, infer_datetime_format=True)
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
                in_data = pd.to_datetime(
                    array_data.data, infer_datetime_format=True)
                array_data.data = in_data
            elif isinstance(array_data.data[0], pd.datetime):
                in_data = array_data.data
            else:
                print("Array data type not understood for comparing date time")
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
        return self.createResult(out, keyword_list, create_name)

    def evaluateForNumbers(self, array_data, target, keyword_list,
                           create_name=True):
        print("Target: ", target.data)
        out = np.full(array_data.shape, True)
        unresolved_idx = np.full(array_data.shape, True)
        self.updateOutput(out, array_data, target.data, unresolved_idx)
        return self.createResult(out, keyword_list, create_name)


class LessThanEqual(LessThan):

    def __init__(self):
        super(LessThanEqual, self).__init__(["equal", "less than",
                                             "smaller than", "before or"],
                                            '<=')


class GreaterThan(LessThan):

    def __init__(self):
        super(GreaterThan, self).__init__(["greater than", "bigger than",
                                           "after"], '>')


class GreaterThanEqual(LessThan):

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
                print("Cannot find enough numbers. Please provide two numbers")
                return ResultObject(None, None, None, CommandStatus.Error)
            if isinstance(array_data.data[0], str):
                date_time = pd.to_datetime(
                    array_data.data, infer_datetime_format=True)
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
                in_data = pd.to_datetime(array_data.data,
                                         infer_datetime_format=True)
                array_data.data = in_data
            elif isinstance(array_data.data[0], pd.datetime):
                in_data = array_data.data
            else:
                print("Array data type not understood for comparing date time")
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


class Outside(AbstractCommand):
    """
    create logical array with elements outside
    specified values
    """
    between = Between()

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


class Contains(AbstractCommand):
    """
    create logical array with elements containing specified text
    """

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
        for word in word_list:
            target_lower = target.lower()
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

# Combine conditions


class LogicalAnd(AbstractCommand):
    """
    combine two logical arrays
    """

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
        print("Performing logical", self._add_tags[0], "on ")
        print(array_data[0].name)
        if self._operator == '!':
            out = np.logical_not(array_data[0].data)

        for arr_data in array_data[1:]:
            print(", ", arr_data.name)
            if self._operator == '&':
                out = np.logical_and(out, arr_data.data)
            elif self._operator == '||':
                out = np.logical_or(out, arr_data.data)
            elif self._operator == '^':
                out = np.logical_xor(out, arr_data.data)
            else:
                return ResultObject(None, None, None, CommandStatus.Error)
            print(arr_data.name)
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


class LogicalOr(LogicalAnd):

    def __init__(self):
        super(LogicalOr, self).__init__(["or"], '||')


class LogicalNot(LogicalAnd):

    def __init__(self):
        super(LogicalNot, self).__init__(["not"], '!')


class LogicalXor(LogicalAnd):

    def __init__(self):
        super(LogicalXor, self).__init__(["xor"], '^')
