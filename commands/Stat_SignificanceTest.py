#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 00:33:34 2018

@author: vishwaparekh
"""

#!/usr/bin/env python2
"""
Define ttest calculator command
"""
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
#from Alfarvis.commands.read_data import ReadData
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.Toolboxes.VariableStore.VarStore import VarStore
import re
import scipy

class StatSigTest(AbstractCommand):
    """
    Calculates ttest for a predictor variable
    """

    def commandTags(self):
        """
        return tags that are used to identify ttest command
        """
        return ["ttest", "p","value"]

    def argumentTypes(self):
        """
        A list of  argument objects that specify the inputs needed for executing
        the ttest command
        """
        return [Argument(keyword="array_data", optional=True, 
                         argument_type=DataType.array)]
    def evaluate(self, array_data=None):
        """
        Calculate ttest of the array and store it to history
        Parameters:
            
        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if array_data is not None:
            keyword_list = array_data.keyword_list
            VarStore.SetCurrentArray(array_data.data," ".join(keyword_list))                    
        else:
            #This will split the sentence into multiple keywords using anything except
            #a-z,0-9 and + as a partition
            pattern = re.compile('[^a-z0-9]+')
            keyword_list = pattern.split(VarStore.currArray_name)    
            
        ground_truth = VarStore.Y
        # TODO: THis will only run if the ground truth has only two labels
        a = VarStore.currArray[ground_truth==1]
        b = VarStore.currArray[ground_truth==2]
        ttest_val= scipy.stats.ttest_ind(a, b, axis=0, equal_var=False)
               
        print("p value for prediction of ", VarStore.label_header, "using ",  
              " ".join(keyword_list), " is ", ttest_val.pvalue)
        result_object = ResultObject(ttest_val.pvalue, keyword_list, 
                                     DataType.array, CommandStatus.Success)
            

        return result_object    
