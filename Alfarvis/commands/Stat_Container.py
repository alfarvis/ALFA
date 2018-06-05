#!/usr/bin/env python3
import numpy as np


class StatContainer(object):
    """
    Container for storing states of different statistics
    commands. For example storing the ground truth or
    output of commands etc
    """
    ground_truth = None
    percCutoff_for_categorical = 0.1

    @classmethod
    def isCategorical(self, array):
        """
        Check if a array is categorical
        """
        try:
            uniqVals = np.unique(array)
        except:
            return False
        if (len(uniqVals) / len(array)) < self.percCutoff_for_categorical:
            return True
        return False
