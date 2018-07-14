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
    conditional_array = None
    percCutoff_for_categorical = 0.1

    @classmethod
    def filterGroundTruth(self):
        if self.ground_truth is None:
            return None
        elif self.conditional_array is None:
            return self.ground_truth.data
        else:
            inds = self.conditional_array.data
            return self.ground_truth.data[inds]
        return None

    @classmethod
    def removeCommonNames(self, input_names):
        """
        Remove common occurences between different strings
        """
        name_set_list = [set(splitPattern(name)) for name in input_names]
        if len(input_names) == 1:
            out_names = ['']
            common_name = ' '.join(name_set_list[0])
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
        if N > 0:
            if hasattr(array, 'iloc'):
                first_val = array.iloc[0]
            else:
                first_val = array[0]
            if ((isinstance(first_val, str) and Nunique < 50) or
                (Nunique / N) <= self.percCutoff_for_categorical):
                return uniqVals
        return None
