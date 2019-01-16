# here we will import the libraries used for machine learning
import numpy as np  # linear algebra
# data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import pandas as pd
import importlib
import collections
import matplotlib.pyplot as plt
import itertools
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, DataObject)
from Alfarvis.commands.Stat_Container import StatContainer
from Alfarvis.printers import Printer
from lazyasd import lazyobject
from scipy.stats import mode
import re

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.linear_model import LogisticRegression  # to apply the Logistic regression
from sklearn.model_selection import train_test_split # to split the data into two parts
from sklearn.model_selection import GridSearchCV# for tuning parameter
from sklearn.ensemble import RandomForestClassifier  # for random forest classifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm  # for Support Vector Machine
from sklearn import preprocessing
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import StratifiedKFold



@lazyobject
def cluster():
    return importlib.import_module('sklearn.cluster')


#@lazyobject
#def StratifiedKFold():
#    return importlib.import_module('sklearn.model_selection.StratifiedKFold')


@lazyobject
def metrics():
    return importlib.import_module('sklearn.metrics')  # for the check the error and accuracy of the model


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
    def transformArray_to_dataFrame(self, array_datas, useCategorical=False, expand_single=False,
                                    remove_nan=False):
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
        if StatContainer.conditional_array is not None and len(StatContainer.conditional_array.data) == array_size:
            inds = StatContainer.conditional_array.data
            Nfiltered = np.sum(inds)
            Printer.Print("Nfiltered: ", Nfiltered)
        else:
            Nfiltered = array_size
            inds = np.full(Nfiltered, True)

        for i, array_data in enumerate(array_datas):
            # Check if the array is a numeric type or not
            if (np.issubdtype(array_data.data.dtype, np.number)) == False:
                if not useCategorical:
                    Printer.Print(
                        "Skipping ", " ".join(array_data.keyword_list),
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
                    Printer.Print("Skipping array ",
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
            Printer.Print("No arrays found in the arguments provided")
            command_status = CommandStatus.Error
        if remove_nan:
            df.dropna(inplace=True)
        return command_status, df, df.columns.values.tolist(), common_name

    @classmethod
    def convertStrCols_toNumeric(self,df):
        for col in df.columns:
            if (np.issubdtype(df[col], np.number)) == False:
                arr_data = pd.Series(df[col])
                lut = dict(zip(arr_data.unique(), np.linspace(0, 1, arr_data.unique().size)))
                # Creating a new data object by mapping strings to numbers
                df[col] = arr_data.map(lut)
        return df
    
    @classmethod
    def removenan(self, df, gt):
        df['ground_truth'] = gt
        df.dropna(inplace=True)
        gt_mod = df['ground_truth']
        df.drop('ground_truth', axis=1, inplace=True)
        return df, gt_mod

    @classmethod
    def standardizeDataFrame(self, df):
        df = (df - df.mean()) / df.std()
        return df

    @classmethod
    def readAlgorithm(self, file_path):
        data = pd.read_csv(file_path)
        model = eval(data['Model'][0])
        for column in data.columns:
            str1 = "model." + str(column)
            str2 = str(data[column][0])
            if str2 == 'TRUE':
                str2 = 'True'
            if str2 == 'FALSE':
                str2 = 'False'
            str_to_evaluate = str1 + " = " + str2
            exec(str_to_evaluate)
        return model

    @classmethod
    def runKFoldCV(self, X, Y, model, num_folds=10):

        # Setting a seed for randomly splitting the data for k fold CV
        seed = 3
        np.random.seed(seed)

        # Getting the training and testing splits for CV
        kfold = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=seed)
        cvscores = []
        aucscores = []

        allTrue = []
        allPred = []
        for train, test in kfold.split(X, Y):

            # Get the training and test dataset for this run
            X_train = X[train]
            X_test = X[test]

            # Fit the model
            model.fit(X_train, Y[train])
            # evaluate the model
            scores = model.score(X_test, Y[test])
            Y_Pr = model.predict_proba(X_test)
            cvscores.append(scores * 100)
            #fpr, tpr, thresholds = metrics.roc_curve(Y[test], Y_Pr[:, 0], pos_label=1)
            #auc_val = metrics.auc(fpr, tpr)
            # aucscores.append(auc_val)

            allTrue = allTrue + (list(Y[test]))
            allPred = allPred + (list(model.predict(X_test)))
        allTrue = np.array(allTrue) - 1
        allPred = np.array(allPred) - 1
        #TP,FP,TN,FN = self.perf_measure(self,allTrue,allPred)
        #Sens = TP/(TP+FN)
        #Spec = TN/(FP+TN)

        cm = metrics.confusion_matrix(allTrue, allPred)

        #Printer.Print("%d-fold cross validation accuracy -  %.2f%% (+/- %.2f%%)" % (num_folds, np.mean(cvscores), np.std(cvscores)))
        #Printer.Print("%d-fold cross validation AUC -  %.2f (+/- %.2f)" % (num_folds, np.mean(aucscores), np.std(aucscores)))
        #Printer.Print("%d-fold cross validation Sens -  %.2f " % (num_folds, Sens, ))
        #Printer.Print("%d-fold cross validation Spec -  %.2f " % (num_folds, Spec, ))

        return cm, cvscores
    
    @classmethod
    def runLOOCV(self, X, Y, model):

        # Setting a seed for randomly splitting the data for k fold CV
        seed = 3
        np.random.seed(seed)

        # Getting the training and testing splits for CV        
        loo = LeaveOneOut()
        cvscores = []
        aucscores = []

        allTrue = []
        allPred = []
        for train, test in loo.split(X, Y):

            # Get the training and test dataset for this run
            X_train = X[train]
            X_test = X[test]

            # Fit the model
            model.fit(X_train, Y[train])
            # evaluate the model
            scores = model.score(X_test, Y[test])
            Y_Pr = model.predict_proba(X_test)
            cvscores.append(scores * 100)
            #fpr, tpr, thresholds = metrics.roc_curve(Y[test], Y_Pr[:, 0], pos_label=1)
            #auc_val = metrics.auc(fpr, tpr)
            # aucscores.append(auc_val)

            allTrue = allTrue + (list(Y[test]))
            allPred = allPred + (list(model.predict(X_test)))
        allTrue = np.array(allTrue) - 1
        allPred = np.array(allPred) - 1
        #TP,FP,TN,FN = self.perf_measure(self,allTrue,allPred)
        #Sens = TP/(TP+FN)
        #Spec = TN/(FP+TN)

        cm = metrics.confusion_matrix(allTrue, allPred)

        #Printer.Print("%d-fold cross validation accuracy -  %.2f%% (+/- %.2f%%)" % (num_folds, np.mean(cvscores), np.std(cvscores)))
        #Printer.Print("%d-fold cross validation AUC -  %.2f (+/- %.2f)" % (num_folds, np.mean(aucscores), np.std(aucscores)))
        #Printer.Print("%d-fold cross validation Sens -  %.2f " % (num_folds, Sens, ))
        #Printer.Print("%d-fold cross validation Spec -  %.2f " % (num_folds, Spec, ))

        return cm, cvscores

    @classmethod
    def FindBestClassifier(self, X, Y, modelList, num_folds):
        all_cv_scores = []
        all_mean_cv_scores = []
        all_confusion_matrices = []
        for i in range(len(modelList)):
            cm, cvscores = (DataGuru.runKFoldCV(X, Y, modelList[i]['Model'], num_folds))
            all_cv_scores.append(cvscores)
            all_mean_cv_scores.append(np.mean(cvscores))
            all_confusion_matrices.append(cm)
        return all_cv_scores, all_mean_cv_scores, all_confusion_matrices

    @classmethod
    def removeGT(self, data_frame, ground_truth):
        pattern = re.compile('[^a-zA-Z0-9]+')
        all_caps_pattern = re.compile('^[^a-z]*$')
        col_head_pattern = re.compile('Unnamed: [0-9]+')
        kl = ground_truth.keyword_list
        col_to_drop = []
        for column in data_frame.columns:
            if col_head_pattern.match(column):
                col_split = column
            elif all_caps_pattern.match(column):
                col_split = [key_val.lower()
                             for key_val in pattern.split(column)]
            else:
                # Add space before upper case
                re.sub(r"([A-Z])", r" \1", column)
                col_split = [key_val.lower()
                             for key_val in pattern.split(column)]

            match_found = 0
            for str in col_split:
                if str in kl:
                    match_found = match_found + 1
            if match_found == len(col_split):
                col_to_drop.append(column)
        if len(col_to_drop) > 0:
            data_frame = data_frame.drop(columns=col_to_drop)

        return data_frame

    @classmethod
    def plot_confusion_matrix(self, cm, classes, ax=plt,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        This method has been copied from scikit toolbox webpage
        http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
        """
        # cm is confusion matrix
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            Printer.Print("Normalized confusion matrix")
        else:
            Printer.Print('Confusion matrix, without normalization')

        Printer.Print(cm)

        ax.imshow(cm, interpolation='nearest', cmap=cmap)
        ax.set_title(title)
        #ax.colorbar()
        #tick_marks = np.arange(len(classes))
        #ax.xticks(tick_marks, classes, rotation=45)
        #ax.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        #ax.tight_layout()
        ax.set_ylabel('True label')
        ax.set_xlabel('Predicted label')

    def perf_measure(self, y_actual, y_hat):
        TP = 0
        FP = 0
        TN = 0
        FN = 0

        for i in range(len(y_hat)):
            if y_actual[i] == y_hat[i] == 1:
                TP += 1
            if y_hat[i] == 1 and y_actual[i] != y_hat[i]:
                FP += 1
            if y_actual[i] == y_hat[i] == 0:
                TN += 1
            if y_hat[i] == 0 and y_actual[i] != y_hat[i]:
                FN += 1
        return (TP, FP, TN, FN)
