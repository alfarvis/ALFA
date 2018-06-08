# here we will import the libraries used for machine learning
import numpy as np  # linear algebra
from scipy.stats import mode
# data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import pandas as pd
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
# from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
# from sklearn.model_selection import train_test_split # to split the data into two parts
#from sklearn.model_selection import StratifiedKFold
# from sklearn.model_selection import GridSearchCV# for tuning parameter
# from sklearn.ensemble import RandomForestClassifier # for random forest classifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.tree import DecisionTreeClassifier
# from sklearn import svm # for Support Vector Machine
# from sklearn import metrics # for the check the error and accuracy of the model
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
    def transformArray_to_dataFrame(self, array_datas):
        # Create a combined array and keyword list
        kl1 = []
        array_sizes = []
        for array_data in array_datas:
            if array_data.data.size != 1:
                array_sizes.append(array_data.data.size)
        if len(array_sizes) == 0:
            array_sizes = [1]
        array_size = mode(array_sizes)[0][0]
        df = pd.DataFrame()
        command_status = CommandStatus.Success
        # TODO Remove outlier arrays using Ransac
        # rather than choosing the array size as the first
        # array size

        for array_data in array_datas:
            if (np.issubdtype(array_data.data.dtype, np.number)) == False:
                print("Skipping ", " ".join(array_data.keyword_list),
                      "\nThe array is not of numeric type")
                continue
            kl1.append(" ".join(array_data.keyword_list))
            if array_size != array_data.data.size:
                if array_data.data.size == 1:
                    data = np.ones(array_size) * array_data.data
                else:
                    print("Skipping array ",
                          " ".join(array_data.keyword_list),
                          " since its size does not match with",
                          " other arrays in the frame")
                    continue
            elif array_data.data.size == 1:
                data = [array_data.data]
            else:
                data = array_data.data
            df[(" ".join(array_data.keyword_list))] = pd.Series(data)

        return command_status, df, kl1

    @classmethod
    def standardizeDataFrame(self, df):
        df = (df - df.mean()) / df.std()
        return df
