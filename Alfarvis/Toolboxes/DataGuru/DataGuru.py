# here we will import the libraries used for machine learning
import numpy as np  # linear algebra
from scipy.stats import mode
# data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import pandas as pd
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, DataObject)
from Alfarvis.commands.Stat_Container import StatContainer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import collections
# from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
# from sklearn.model_selection import train_test_split # to split the data into two parts
from sklearn.model_selection import StratifiedKFold
# from sklearn.model_selection import GridSearchCV# for tuning parameter
# from sklearn.ensemble import RandomForestClassifier # for random forest classifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.tree import DecisionTreeClassifier
from sklearn import svm  # for Support Vector Machine
from sklearn import metrics  # for the check the error and accuracy of the model
from sklearn import preprocessing
from sklearn.model_selection import LeaveOneOut
import re


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
    def transformArray_to_dataFrame(self, array_datas, useCategorical=False, expand_single=False):
        # Create a combined array and keyword list
        array_sizes = []
        # Check if array_datas is of length 1 or not
        if not isinstance(array_datas, collections.Iterable):
            array_datas = [array_datas]
        for array_data in array_datas:
            if array_data.data.size != 1:
                array_sizes.append(array_data.data.size)
        if len(array_sizes) == 0:
            array_sizes = [1]
        array_size = mode(array_sizes)[0][0]
        df = pd.DataFrame()
        command_status = CommandStatus.Success
        kl1 = [" ".join(array_data.keyword_list) for array_data in array_datas]
        truncated_kl1, common_name = StatContainer.removeCommonNames(kl1)
        # Conditional filter
        if StatContainer.conditional_array is not None:
            inds = StatContainer.conditional_array.data
            Nfiltered = np.sum(inds)
            print("Nfiltered: ", Nfiltered)
        else:
            Nfiltered = array_size
            inds = np.full(Nfiltered, True)

        for i, array_data in enumerate(array_datas):
            # Check if the array is a numeric type or not
            if (np.issubdtype(array_data.data.dtype, np.number)) == False:
                if not useCategorical:
                    print("Skipping ", " ".join(array_data.keyword_list),
                          "\nThe array is not of numeric type")
                    continue
                else:
                    if len(array_datas) > 1:
                        # Map the array to numeric quantity
                        arr_data = pd.Series(array_data.data[inds])
                        lut = dict(zip(arr_data.unique(), np.linspace(0, 1, arr_data.unique().size)))
                        # Creating a new data object by mapping strings to numbers
                        array_data = DataObject(arr_data.map(lut), array_data.keyword_list)

            # Check if all the arrays have the same size or not. Pick the largest
            # set of arrays that have the same size
            if array_size != array_data.data.size:
                if array_data.data.size == 1 and expand_single:
                    data = np.ones(Nfiltered) * array_data.data
                else:
                    print("Skipping array ",
                          " ".join(array_data.keyword_list),
                          " since its size does not match with",
                          " other arrays in the frame")
                    continue
            elif array_data.data.size == 1:
                data = [array_data.data]
            else:
                data = array_data.data[inds]
            df[truncated_kl1[i]] = pd.Series(data)

        if df.size == 0:
            print("No arrays found in the arguments provided")
            command_status = CommandStatus.Error
        return command_status, df, df.columns.values.tolist(), common_name

    @classmethod
    def standardizeDataFrame(self, df):
        df = (df - df.mean()) / df.std()
        return df
