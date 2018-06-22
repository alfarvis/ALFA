#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 15:34:47 2018

@author: gowtham
"""

from Alfarvis.commands.find_inliers import findInliers
import matplotlib.pyplot as plt
import numpy as np

#data = np.random.sample((100,2))*10
data = np.vstack((np.random.sample((100,2)), np.random.sample((20,2))+1.5, np.random.sample((20,2))+1))
inliers = findInliers(data)
# %%
plt.figure(1)
plt.plot(data[:,0], data[:, 1], 'b*')
if inliers is not None:
    plt.plot(data[inliers,0], data[inliers,1], 'r*')
# %%
plt.figure(2)
plt.plot(data[inliers,0], data[inliers,1], 'b*')

