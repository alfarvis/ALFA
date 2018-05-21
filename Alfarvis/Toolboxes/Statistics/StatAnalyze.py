#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 16:07:25 2018

@author: vishwaparekh
"""

class DataAnalyze:
    """
    Data Analysis toolbox for data exploration and visualization
    Functionalities supported
    
        
    
    """
    def __init__(self, data_path,label_header):
        """
        Constructor method to initialize the class with a default data set for analysis
        """
        self.data = pd.read_csv(data_path)
        datas = pd.DataFrame(self.data)
        datas.columns = list(self.data.columns)
        