# here we will import the libraries used for machine learning
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import matplotlib.pyplot as plt # this is used for the plot the graph
import seaborn as sns # used for plot interactive graph. I like it most for plot


class VarStore:

    """
    Contains current memory of all kinds of variables
    """
    
    @classmethod
    def SetCurrentCSV(self,data,name):
        
        self.CurrCSV = data
        self.CurrCSV_name = name
        
        label_header=self.CurrCSV.columns[0]
        self.label_header = label_header
        print("label header:", label_header)
        datas = pd.DataFrame(self.CurrCSV)
        datas.columns = list(self.CurrCSV.columns)
        data_drop = datas.drop(label_header,axis=1)
        self.X = data_drop.values
        self.Y =  datas[label_header]
        self.columnList = self.CurrCSV.columns[1:]
        # Cleaning and standardizing data
    
    @classmethod
    def SetCurrentArray(self,data,name):
        self.currArray = data
        self.currArray_name = name
    
    @classmethod    
    def SetCurrentImage(self,data,name):
        print("I was here")
        self.currImg = data
        self.currImg_name = name
        

 