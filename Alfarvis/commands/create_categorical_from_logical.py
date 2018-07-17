#!/usr/bin/env python3
"""
Created on Mon Jul 16 21:12:19 2018

@author: gowtham
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Stat_Container import StatContainer
import numpy as np
import collections

# create categorical from conditional arrays


class CreateCategoricalFromLogical(AbstractCommand):
    def commandTags(self):
        """
        Tags to identify the bar plot command
        """
        return ["create", "categorical", "combine"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the bar plot command
        """
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.logical_array, number=-1)]

    def evaluate(self, array_datas):
        if not isinstance(array_datas, collections.Iterable):
            array_datas = [array_datas]
        N = array_datas[0].data.size
        out = np.full(N, 'Unknown', dtype='S20')
        for array_data in array_datas:
            if array_data.data.size == N:
                out[array_data.data] = array_data.name
        kl1 = [" ".join(array_data.keyword_list) for array_data in array_datas]
        truncated_kl1, common_name = StatContainer.removeCommonNames(kl1)
        if common_name == '':
            common_name_list = array_data[0].keyword_list
        else:
            common_name_list = common_name.split(' ')

        result = ResultObject(out, [], DataType.array,
                              CommandStatus.Success)
        result.createName(common_name_list, command_name='categorical',
                          set_keyword_list=True)
        return result
