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
        print("Name:", name, "already in dictionary")
        return False
    return True


def getName(name_list):
    sum_name_list = sum(name_list, [])
    return '.'.join(sum_name_list), sum_name_list


def addKeyword(index, keyword_list, up_list):
    if len(keyword_list) > index and name_pattern.match(keyword_list[index]):
        up_list.append(keyword_list[index])


def createName(name_dict, keyword_list1, keyword_list2=[], command_name=''):
    """
    Create a unique name from given keyword lists
    """
    foundName = False
    command_name_list = []
    first_keyword_list = []
    second_keyword_list = []
    if command_name != '':
        command_name_list.append(command_name)
    addKeyword(0, keyword_list1, first_keyword_list)
    addKeyword(0, keyword_list2, second_keyword_list)
    start_id_klist1 = 1
    if len(keyword_list2) == 0:
        addKeyword(1, keyword_list1, first_keyword_list)
        start_id_klist1 = 2

    comp_list = [command_name_list, first_keyword_list, second_keyword_list]
    name, name_comp = getName(comp_list)
    if not checkName(name, name_dict):
        for keywords in zip_longest(keyword_list1[start_id_klist1:],
                                    keyword_list2[1:], fillvalue='-'):
            if foundName:
                break
            for i, keyword in enumerate(keywords):
                if name_pattern.match(keyword):
                    comp_list[i + 1].append(keyword)
                    name, name_comp = getName(comp_list)
                    if checkName(name, name_dict):
                        foundName = True
                        break
    else:
        foundName = True
    if not foundName:
        comp_list.append(['1'])
        for i in range(1000):
            name, name_comp = getName(comp_list)
            if name not in name_dict:
                foundName = True
                break
            comp_list[-1][0] = str(i + 2)
    if foundName:
        return name, name_comp
    raise RuntimeError("Cannot find a unique name")
