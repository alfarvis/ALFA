#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 12:07:11 2018

@author: gowtham
"""

import numpy as np


def getMinIndices(array):
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


def findClosestMatch(match_res):
    data_len_list = [data.length for data in match_res]
    idx = getMinIndices(data_len_list)
    if len(idx) == 1:
        return match_res[idx[0]]
    return None
