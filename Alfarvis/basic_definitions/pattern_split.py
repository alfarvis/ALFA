#!/usr/bin/env python3

import re


# This will split the sentence into multiple keywords using anything except
# a-z,0-9 and + as a partition
pattern = re.compile('[^a-zA-Z0-9]+')
all_caps_pattern = re.compile('^[^a-z]*$')


def splitPattern(input_string):
    """
    Split input string based on non-string/non-numeric characters
    or based on caps. Also handles all caps strings correctly
    """
    if all_caps_pattern.match(input_string):
        out_list = [key_val.lower()
                    for key_val in pattern.split(input_string)]
    else:
        # Add space before upper case
        input_string = re.sub(r"([A-Z])", r" \1", input_string)
        out_list = [key_val.lower()
                    for key_val in pattern.split(input_string) if key_val != '']
    return out_list
