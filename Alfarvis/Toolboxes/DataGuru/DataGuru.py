# here we will import the libraries used for machine learning
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
#from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
#from sklearn.model_selection import train_test_split # to split the data into two parts
#from sklearn.model_selection import StratifiedKFold
#from sklearn.model_selection import GridSearchCV# for tuning parameter
#from sklearn.ensemble import RandomForestClassifier # for random forest classifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.tree import DecisionTreeClassifier
#from sklearn import svm # for Support Vector Machine
#from sklearn import metrics # for the check the error and accuracy of the model
#from sklearn import preprocessing
#from sklearn.model_selection import LeaveOneOut

class DataGuru:

    """
    Run data analytics (exploration and mining) on any structured dataset
    Has the following functionality
        - Find the best algorithm
        - Find the top features
        - k-fold cross validation accuracy
        - transform an array of arrays to a dataframe
    Has the following models
        - Support Vector Machine
        - Random Forest
        - Decision Tree
        - k Nearest Neighbor
        - Feed Forward Neural Network
    """
    @classmethod
    def transformArray_to_dataFrame(self,array_datas):
        #Create a combined array and keyword list
        kl1 =[]
        arrays = []
        array_size = 0
        command_status = CommandStatus.Success
        
        for array_data in array_datas:
            if (np.issubdtype(array_data.data.dtype, np.number))==False:  
                print("Skipping ", " ".join(array_data.keyword_list),
                      "\nThe array is not of numeric type")                
                continue
            kl1.append(" ".join(array_data.keyword_list))
            arrays.append(array_data.data)            
            if array_size == 0:
                array_size = array_data.data.size
                if array_size==1:
                    df = pd.DataFrame({(" ".join(array_data.keyword_list)):[array_data.data]})
                else:
                    df = pd.DataFrame({(" ".join(array_data.keyword_list)):array_data.data})
            else:
                if array_size != array_data.data.size:
                    print("The arrays provided are not of the same dimensions")
                    command_status = CommandStatus.Error
                    break
                df[(" ".join(array_data.keyword_list))] = pd.Series(array_data.data)
            
            
        return command_status, df, kl1
    
    @classmethod
    def standardizeDataFrame(self,df):
        df=(df-df.mean())/df.std()
        return df
