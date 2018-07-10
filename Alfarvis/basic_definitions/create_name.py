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


def createName(name_dict, keyword_list1, keyword_list2=[], command_name=''):
    """
    Create a unique name from given keyword lists
    """
    name_components = []
    if command_name != '':
        name_components.append(command_name)
        sid = 1
    else:
        sid = 0
    for keyword_list in [keyword_list1, keyword_list2]:
        if len(keyword_list) != 0:
            keyword = keyword_list[0]
            if name_pattern.match(keyword):
                name_components.append(keyword)
#    kid = 1
#    if (command_name == '' and len(keyword_list2) == 0 and
#        len(keyword_list1) >= 1):
#            keyword = keyword_list1[1]
#            if name_pattern.match(keyword):
#                if len(name_components) == 0:
#                    name_components = keyword
#                else:
#                name_components[0] = name_components[0] + keyword
    # Try adding second word also if available (Maybe not a good idea!)
    # for i, keyword_list in enumerate([keyword_list1, keyword_list2]):
    #    if len(keyword_list) >= 1:
    #        keyword = keyword_list[1]
    #        if name_pattern.match(keyword):
    #            name_components[i+1] = name_components[i+1] + keyword
    # If using above, change zip to start from 2: instead of 1:
    name = '.'.join(name_components)
    if checkName(name, name_dict):
        return name, name_components
    else:
        zip_object = zip_longest(keyword_list1[1:], keyword_list2[1:],
                                 fillvalue='-')
        for keywords in zip_object:
            if name_pattern.match(keywords[0]):
                name_components[sid] = name_components[sid] + "." + keywords[0]
                name = '.'.join(name_components)
                if checkName(name, name_dict):
                    return name, name_components
            if name_pattern.match(keywords[1]):
                name_components[sid + 1] = name_components[sid + 1] + "." + keywords[1]
                name = '.'.join(name_components)
                if checkName(name, name_dict):
                    return name, name_components
    name_components.append('1')
    for i in range(1000):
        name = '.'.join(name_components)
        if name not in name_dict:
            return name, name_components
        name_components[-1] = str(i + 2)
    raise RuntimeError("Cannot find a unique name")
