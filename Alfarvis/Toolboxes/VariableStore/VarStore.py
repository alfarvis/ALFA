# here we will import the libraries used for machine learning
#import numpy as np  # linear algebra
# data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import pandas as pd


class VarStore:

    """
    Contains current memory of all kinds of variables
    """

    @classmethod
    def SetCurrentCSV(self, data, name):

        self.currCSV = data
        self.currCSV_name = name
        datas = pd.DataFrame(self.currCSV)
        self.datas = datas
        datas.columns = list(self.currCSV.columns)
        self.X = datas.values
        self.columnList = self.currCSV.columns[0:]

    @classmethod
    def SetCurrentArray(self, data, name):
        self.currArray = data
        self.currArray_name = name

    @classmethod
    def SetCurrentImage(self, data, name):
        self.currImg = data
        self.currImg_name = name
        
    @classmethod
    def SetGroundTruth(self,data,name):
        self.label_header = name
        self.Y = data
