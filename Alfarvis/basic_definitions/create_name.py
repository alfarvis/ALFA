#!/usr/bin/env python3
"""
Created on Tue Jul 10 07:49:39 2018

@author: gowtham
"""

from itertools import zip_longest
import re

name_pattern = re.compile('^[a-zA-Z0-9.]*$')


def checkName(name, name_dict):
    if name in name_dict:
        return False
    return True


def getName(name_list):
    sum_name_list = sum(name_list, [])
    return '.'.join(sum_name_list), sum_name_list


def addKeyword(keyword, up_list):
    keyword_s = keyword.split(' ', 1)[0]
    if name_pattern.match(keyword_s):
        up_list.append(keyword_s)


def createName(name_dict, keyword_list1, keyword_list2=[], command_name=''):
    """
    Create a unique name from given keyword lists
    """
    foundName = False
    # Remove common keywords from the second keyword list
    #keyword_list2_mod = [keyword for keyword in keyword_list2 if keyword not in keyword_list1]
    # if keyword_list2_mod == []:
    #    # If keyword list2 is part of first one can remove first
    #    keyword_list2 = []
    # else:
    #    keyword_list2 = keyword_list2_mod
    command_name_list = []
    first_keyword_list = []
    second_keyword_list = []
    if command_name != '':
        command_name_list = command_name.split(' ')
    if type(keyword_list1) == str:
        keyword_list1 = keyword_list1.split(' ')
    for i, keyword in enumerate(keyword_list1):
        addKeyword(keyword, first_keyword_list)
    for i, keyword in enumerate(keyword_list2):
        addKeyword(keyword, second_keyword_list)
    comp_list = [command_name_list, first_keyword_list, second_keyword_list]
    name, name_comp = getName(comp_list)
    additional_keyword_added = False
    if checkName(name, name_dict):
        foundName = True
    else:
        comp_list.append(['1'])
        for i in range(1000):
            name, name_comp = getName(comp_list)
            if name not in name_dict:
                foundName = True
                break
            comp_list[-1][0] = str(i + 2)
        additional_keyword_added = True
    if foundName:
        name = name.lower()
        return name, name_comp, additional_keyword_added
    raise RuntimeError("Cannot find a unique name")
