#!/usr/bin/env python3
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern)
from .abstract_command import AbstractCommand
from .argument import Argument

import numpy as np

# Conditional commands


class LessThan(AbstractCommand):
    """
    create logical array with elements less than
    specified value
    """

    def __init__(self, condition=["less", "smaller"], operator='<'):
        self._condition = condition
        self._operator = operator

    def commandTags(self):
        """
        Tags to identify the condition
        """
        return self._condition + [self._operator, "condition", "conditional",
                                  "logical", "logic", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         tags=[Argument.Tag('than',
                                            Argument.TagPosition.After),
                               Argument.Tag(self._condition[0],
                                            Argument.TagPosition.After),
                               Argument.Tag(self._operator,
                                            Argument.TagPosition.After)],
                         argument_type=DataType.number)]

    def evaluate(self, array_data, target):
        print("Target: ", target.data)
        idx = np.logical_not(np.isnan(array_data.data))
        out = np.full(array_data.data.shape, False)
        if self._operator == '<':
            out[idx] = array_data.data[idx] < target.data
        elif self._operator == '<=':
            out[idx] = array_data.data[idx] <= target.data
        elif self._operator == '>':
            out[idx] = array_data.data[idx] > target.data
        elif self._operator == '>=':
            out[idx] = array_data.data >= target.data
        else:
            return ResultObject(None, None, None, CommandStatus.Error)
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
        result.createName(array_data.keyword_list,
                          command_name=self._condition[0],
                          set_keyword_list=True)
        return result


class LessThanEqual(LessThan):

    def __init__(self):
        super(LessThanEqual, self).__init__(["less", "lesser", "equal"], '<=')


class GreaterThan(LessThan):

    def __init__(self):
        super(GreaterThan, self).__init__(["greater", "bigger"], '>')


class GreaterThanEqual(LessThan):

    def __init__(self):
        super(GreaterThanEqual, self).__init__(["greater", "bigger" "equal"], '>=')


# in between
class Between(AbstractCommand):
    """
    create logical array with elements between
    specified values
    """

    def commandTags(self):
        """
        Tags to identify the condition
        TODO: Check if we can less and greater together?
        """
        return ["between", "inside", "range", "condition",
                "conditional", "logical", "logic", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         tags=[Argument.Tag('between',
                                            Argument.TagPosition.After),
                               Argument.Tag('inside',
                                            Argument.TagPosition.After),
                               Argument.Tag('range',
                                            Argument.TagPosition.After),
                               Argument.Tag('(',
                                            Argument.TagPosition.After)],
                         number=2,
                         argument_type=DataType.number)]

    def evaluate(self, array_data, target):
        print("Finding range between: ", target[0].data, target[1].data)
        idx = np.logical_not(np.isnan(array_data.data))
        out = np.full(array_data.data.shape, False)
        out[idx] = (array_data.data[idx] > target[0].data)
        out[idx] = np.logical_and(out[idx], (array_data.data[idx] < target[1].data))
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
        result.createName(array_data.keyword_list, command_name='between',
                          set_keyword_list=True)
        return result


class Outside(AbstractCommand):
    """
    create logical array with elements outside
    specified values
    """

    def commandTags(self):
        """
        Tags to identify the condition
        TODO: Check if we can less and greater together?
        """
        return ["outside", "not", "range", "(", ")", "condition",
                "conditional", "logical", "logic", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         tags=[Argument.Tag('outside',
                                            Argument.TagPosition.After),
                               Argument.Tag('range',
                                            Argument.TagPosition.After),
                               Argument.Tag('(',
                                            Argument.TagPosition.After)],
                         number=2,
                         argument_type=DataType.number)]

    def evaluate(self, array_data, target):
        idx = np.logical_not(np.isnan(array_data.data))
        out = np.full(array_data.data.shape, False)
        out[idx] = (array_data.data[idx] < target[0].data)
        out[idx] = np.logical_and(out[idx], (array_data.data[idx] > target[0].data))
        result = ResultObject(out, [], DataType.logical_array,
                              CommandStatus.Success, True)
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
        return ["contains", "condition",
                "conditional", "logical", "logic", "create"]

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
            if word in target:
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
        return self._add_tags + [self._operator, "logical", "logic", "create"]

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
        for arr_data in array_data[1:]:
            if self._operator == '&':
                out = np.logical_and(out, arr_data.data)
            elif self._operator == '||':
                out = np.logical_or(out, arr_data.data)
            elif self._operator == '!':
                out = np.logical_not(out, arr_data.data)
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


# create categorical from conditional arrays
