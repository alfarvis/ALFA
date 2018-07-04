#!/usr/bin/env python3
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Viz_Container import VizContainer

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
                               Argument.Tag(self._operator,
                                            Argument.TagPosition.After)],
                         argument_type=DataType.number)]

    def evaluate(self, array_data, target):
        if self._operator == '<':
            out = array_data.data < target.data
        elif self._operator == '<=':
            out = array_data.data <= target.data
        elif self._operator == '>':
            out = array_data.data > target.data
        elif self._operator == '>=':
            out = array_data.data >= target.data
        else:
            return ResultObject(None, None, None, CommandStatus.Error)
        keyword_set = set(array_data.keyword_list)
        self.addCommandToKeywords(keyword_set)
        return ResultObject(out, keyword_set, DataType.logical_array,
                            CommandStatus.Success)


class LessThanEqual(LessThan):

    def __init__(self):
        super(LessThanEqual, self).__init__(["less", "lesser", "equal"], '<=')


class GreaterThan(LessThan):

    def __init__(self):
        super(GreaterThan, self).__init__(["greater", "bigger"], '>')


class GreaterThanEqual(LessThan):

    def __init__(self):
        super(GreaterThanEqual, self).__init__(["greater", "equal"], '>=')


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
        return ["between", "inside", "range", "(", ")", "condition",
                "conditional", "logical", "logic", "create"]

    def argumentTypes(self):
        return [Argument(keyword="array_data", optional=True,
                argument_type=DataType.array),
                Argument(keyword="target", optional=False,
                         tags=[Argument.Tag('between',
                                            Argument.TagPosition.After),
                               Argument.Tag('range',
                                            Argument.TagPosition.After),
                               Argument.Tag('(',
                                            Argument.TagPosition.After)],
                         number=2,
                         argument_type=DataType.number)]

    def evaluate(self, array_data, target):
        out = (array_data.data > target[0].data)
        out = np.logical_and(out, (array_data.data < target[0].data))
        keyword_set = set(array_data.keyword_list)
        self.addCommandToKeywords(keyword_set)
        return ResultObject(out, keyword_set, DataType.logical_array,
                            CommandStatus.Success)


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
        out = (array_data.data < target[0].data)
        out = np.logical_and(out, (array_data.data > target[0].data))
        keyword_set = set(array_data.keyword_list)
        self.addCommandToKeywords(keyword_set)
        return ResultObject(out, keyword_set, DataType.logical_array,
                            CommandStatus.Success)

# contains


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
            data, split_target) for data in array_data])
        keyword_set = set(array_data.keyword_list)
        keyword_set.update(split_target)
        return ResultObject(out, keyword_set, DataType.logical_array,
                            CommandStatus.Success)

# set condition for filtering data when plotting etc

# create categorical from conditional arrays
