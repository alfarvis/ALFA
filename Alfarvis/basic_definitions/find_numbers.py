#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 16:43:17 2018

@author: gowtham
"""
from .data_object import DataObject


def getNumber(string_in):
    """
    Convert string to number if possible.
    """
    try:
        res = float(string_in)
    except:
        res = None
    return res


def findNumbers(keyword_list, N):
    """
    Find numbers from given keyword list. Will search for N
    arguments
    """
    data_res = []
    for keyword in keyword_list:
        res = getNumber(keyword)
        if res is not None:
            data_res.append(DataObject(res, []))
        if len(data_res) == N:
            break
    return data_res
