#!/usr/bin/env python3
"""
Created on Sun Jul 15 15:53:09 2018

@author: gowtham
"""
from Alfarvis.basic_definitions.search_date_time import searchDateTime

input_text = 'between 9 pm on 06/23/1991 and 10:45 am on 5 may 1940'
out = searchDateTime(input_text.split(' '))
print(out)
