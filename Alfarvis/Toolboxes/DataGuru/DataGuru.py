# here we will import the libraries used for machine learning
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
#from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
#from sklearn.model_selection import train_test_split # to split the data into two parts
from sklearn.model_selection import StratifiedKFold
#from sklearn.model_selection import GridSearchCV# for tuning parameter
from sklearn.ensemble import RandomForestClassifier # for random forest classifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.tree import DecisionTreeClassifier
#from sklearn import svm # for Support Vector Machine
from sklearn import metrics # for the check the error and accuracy of the model
from sklearn import preprocessing
from sklearn.model_selection import LeaveOneOut

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
                    print("The arrays to be plotted are not of the same dimensions")
                    command_status = CommandStatus.Error
                    break
                df[(" ".join(array_data.keyword_list))] = pd.Series(array_data.data)
            if (np.issubdtype(array_data.data.dtype, np.number))==False:  
                print("Please provide numeric arrays")
                command_status = CommandStatus.Error
                break
            
        return command_status, df, kl1
            
    # Create a generic classification model to work with any classifier
    def classification_model(self,model,num_folds,topFeatures=0):
        X = self.X
        Y = self.Y
        if (topFeatures!=0):
            X = X[:,0:topFeatures]
        # Model is the classification model
        # X - input data
        # Y - output labels
        # num_folds - number of folds to use for k-fold cross validation

        # First check the classification accuracy on training data
          # Here we fit the model using training set
        # Make predictions on training set:
        model.fit(X, Y)
        predictions = model.predict(X)
        accuracy = metrics.accuracy_score(predictions, Y)
        #print("Accuracy on training set : %s" % "{0:.3%}".format(accuracy))

        # Now let us check the accuracy of the test dataset
        seed = 3
        np.random.seed(seed)
        # K fold cross validation (k=2)

        kfold = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=seed)
        cvscores = []
        error = []
        aucscores = []


        allTrue = []
        allPred = []
        for train, test in kfold.split(X, Y):

            #Standardize the train and test dataset
            X_train = X[train]
            X_test = X[test]
            scaler = preprocessing.StandardScaler().fit(X_train)
            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)
            # Fit the model
            model.fit(X_train, Y[train])
            # evaluate the model
            scores = model.score(X_test, Y[test])
            Y_Pr = model.predict_proba(X_test)
            # Print scores from each cross validation run
            # print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
            cvscores.append(scores * 100)
            fpr, tpr, thresholds = metrics.roc_curve(Y[test], Y_Pr[:, 0], pos_label=1)
            auc_val = metrics.auc(fpr, tpr)
            aucscores.append(auc_val)

            allTrue = allTrue + (list(Y[test]))
            allPred = allPred + (list(model.predict(X_test)))
        allTrue = np.array(allTrue)-1
        allPred = np.array(allPred)-1
        TP,FP,TN,FN = self.perf_measure(allTrue,allPred)
        Sens = TP/(TP+FN)
        Spec = TN/(FP+TN)

        print("%d-fold cross validation accuracy -  %.2f%% (+/- %.2f%%)" % (num_folds, np.mean(cvscores), np.std(cvscores)))
        print("%d-fold cross validation AUC -  %.2f%% (+/- %.2f%%)" % (num_folds, np.mean(aucscores), np.std(aucscores)))
        print("%d-fold cross validation Sens -  %.2f%% " % (num_folds, Sens, ))
        print("%d-fold cross validation Spec -  %.2f%% " % (num_folds, Spec, ))

        return np.mean(cvscores), np.mean(aucscores)

    def classification_model_wLOOCV(self,model,topFeatures=0):
        X = self.X
        Y = self.Y
        if (topFeatures!=0):
            X = X[:,0:topFeatures]
        # Model is the classification model
        # X - input data
        # Y - output labels
        # num_folds - number of folds to use for k-fold cross validation

        # First check the classification accuracy on training data
          # Here we fit the model using training set
        # Make predictions on training set:
        model.fit(X, Y)
        predictions = model.predict(X)
        accuracy = metrics.accuracy_score(predictions, Y)
        #print("Accuracy on training set : %s" % "{0:.3%}".format(accuracy))

        # Now let us check the accuracy of the test dataset
        seed = 3
        np.random.seed(seed)
        # K fold cross validation (k=2)
        loo = LeaveOneOut()

        #kfold = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=seed)

        cvscores = []
        error = []
        aucscores = []


        allTrue = []
        allPred = []
        allY_Pr = []
        for train, test in loo.split(X, Y):

            #Standardize the train and test dataset
            X_train = X[train]
            X_test = X[test]
            scaler = preprocessing.StandardScaler().fit(X_train)
            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)
            # Fit the model
            model.fit(X_train, Y[train])
            # evaluate the model
            scores = model.score(X_test, Y[test])
            Y_Pr = model.predict_proba(X_test)
            # Print scores from each cross validation run
            # print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
            cvscores.append(scores * 100)

            allTrue = allTrue + (list(Y[test]))
            allPred = allPred + (list(model.predict(X_test)))
            allY_Pr = allY_Pr + (list(Y_Pr))
        allTrue = np.array(allTrue)-1
        allPred = np.array(allPred)-1
        TP,FP,TN,FN = self.perf_measure(allTrue,allPred)
        Sens = TP/(TP+FN)
        Spec = TN/(FP+TN)
        allY_Pr = np.array(allY_Pr)
        fpr, tpr, thresholds = metrics.roc_curve(Y, allY_Pr[:, 0], pos_label=1)
        auc_val = metrics.auc(fpr, tpr)

        print("%d-fold cross validation accuracy -  %.2f%% (+/- %.2f%%)" % (1, np.mean(cvscores), np.std(cvscores)))
        print("%d-fold cross validation AUC -  %.2f%% " % (1, auc_val))
        print("%d-fold cross validation Sens -  %.2f%% " % (1, Sens, ))
        print("%d-fold cross validation Spec -  %.2f%% " % (1, Spec, ))

        return np.mean(cvscores), np.mean(aucscores)

    # Find the best classifier
    def FindBestClassifier(self,modelList,num_folds,topFeatures=0):



        cdsvores = []
        for i in range(len(modelList)):
            cdsvores1, aucscores = (self.classification_model(modelList[i]['Model'],num_folds,topFeatures))
            cdsvores.append(cdsvores1)

        print("Best classifier is " + modelList[np.argmax(cdsvores)]['Name'] +" with an accuracy of -  %.2f%% " % max(cdsvores))
        print('--------------------------\n--------------------------\n')

    #Find the top predictors
    def FindTopPredictors(self,algoType="RF"):
        X = self.X
        Y = self.Y
        # If the selected algo is RF, find the top features using RF
        featImpVals = self.SortTopFeatures_RF(X,Y)
        # If the selected algo is TTest
        #featImpVals = self.SortTopFeatures_TT(X,Y)
        # If the selected algo is LogReg
        # = self.SortTopFeatures_LR(X,Y)

        self.featimp = pd.Series(featImpVals, index=self.columnList).sort_values(ascending=False)
        print("Here is a sorted list of top features found using the " + algoType + "algorithm")

        print(self.featimp)
        print('--------------------------\n--------------------------\n')
        self.X = self.data[self.featimp.index[0:]].values
        self.columnList = self.featimp.index

    def SortTopFeatures_RF(self,X,Y):
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, Y)
        return model.feature_importances_

    def SortTopFeatures_TT(self,X,Y):
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, Y)
        return model.feature_importances_

    def SortTopFeatures_LR(self,X,Y):
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, Y)
        return model.feature_importances_

    def perf_measure(self,y_actual, y_hat):
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
            if y_hat[i] == 0 and y_actual[i] != y_hat[i]:    FN += 1
        return (TP, FP, TN, FN)