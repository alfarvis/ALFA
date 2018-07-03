#!/usr/bin/env python3
import numpy as np
from Alfarvis.basic_definitions import splitPattern


class StatContainer(object):
    """
    Container for storing states of different statistics
    commands. For example storing the ground truth or
    output of commands etc
    """
    ground_truth = None
    percCutoff_for_categorical = 0.1

    @classmethod
    def removeCommonNames(self, input_names):
        name_set_list = [set(splitPattern(name)) for name in input_names]
        if len(input_names) == 1:
            out_names = [list(name_set_list[0])[0]]
            common_name = out_names[0]
        else:
            common_name_set = set.intersection(*name_set_list)
            common_name = ' '.join(common_name_set)
            out_names = [' '.join(name_set.difference(common_name_set))
                         for name_set in name_set_list]
        return out_names, common_name
            

    @classmethod
    def isCategorical(self, array):
        """
        Check if a array is categorical
        and return the categorical values if unique
        otherwise return None
        """
        try:
            uniqVals = np.unique(array)
        except:
            return None
        Nunique = len(uniqVals)
        N = len(array)
        if N > 0 and isinstance(array[0], str) and Nunique < 50:
            return uniqVals
        elif (Nunique / N) > self.percCutoff_for_categorical:
            return None
        return uniqVals
