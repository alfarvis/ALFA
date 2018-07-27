#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 14:26:34 2018

@author: gowtham
"""

import numpy as np
from Alfarvis.printers import Printer


def findInliers(input_array, inlier_ratio=0.5, cutoff_outlier_gain=1):
    """
    search for inliers in an array based on growing a region around the median.
    Assumes the array is [Nxr]
    """
    median = np.median(input_array, axis=0)
    # Can also try mean above if it works
    distances = np.linalg.norm(input_array - median, axis=1)
    stdev_dist = np.std(distances)
    sort_inds = np.argsort(distances)
    sorted_dist_diff = np.diff(distances[sort_inds])
    i = np.argmax(sorted_dist_diff)
    N = distances.size
    if (sorted_dist_diff[i] > stdev_dist * cutoff_outlier_gain and
        i > N * inlier_ratio):
        Printer.Print("Removing Outliers")
        return sort_inds[:(i + 1)]
    return None
