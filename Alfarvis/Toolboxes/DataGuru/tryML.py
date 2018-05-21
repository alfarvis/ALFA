import numpy as np
from ML_Analyze import MLAnalyze
from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
from sklearn.model_selection import train_test_split # to split the data into two parts
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV# for tuning parameter
from sklearn.ensemble import RandomForestClassifier # for random forest classifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm # for Support Vector Machine
from sklearn import preprocessing

# For breast cancer dataset from kaggle
str1 = 'C:/Users/Adv_Breast2_telsa/PycharmProjects/MachineLearning/data.csv'
str2 = 'diagnosis'

# For Luke's dataset
str1 = 'H:/Research/Data/Brain_Mets/Multiview_IsoSVM_singleTP/Radiomics_64bins_64nL.csv'
str2 = 'Labels'
ml_Analyzer = MLAnalyze(data_path = str1,label_header=str2)
Y = ml_Analyzer.Y
#Y = Y.map({'M':1,'B':2})
ml_Analyzer.Y = np.array(list(Y))
model = svm.SVC(probability=True)
#ml_Analyzer.classification_model(model,10,10)

modelList =[]
modelList.append({'Name':'Logistic Regression','Model':LogisticRegression()})
modelList.append({'Name':'Random Forest','Model':RandomForestClassifier(n_estimators=100)})
modelList.append({'Name':'Decision Tree','Model':DecisionTreeClassifier()})
modelList.append({'Name':'Support Vector Machine','Model':svm.SVC(probability=True)})


#ml_Analyzer.FindBestClassifier(modelList,10,10)

#ml_Analyzer.FindTopPredictors()

#ml_Analyzer.FindBestClassifier(modelList,10,5)

ml_Analyzer.FindTopPredictors()
model = RandomForestClassifier(n_estimators=1000,class_weight = {1:1,2:1})

#param_grid = [
#  {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
#  {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001, 0.01, 0.1], 'kernel': ['rbf']},
# ]

#param_grid = [
#  {'n_estimators': [10, 100, 1000]}
# ]

#model = svm.SVC(probability=True,class_weight = {1:1,2:2},gamma = 0.1)
#model = RandomForestClassifier()
#gsRes = GridSearchCV(model,param_grid,cv=10,scoring="accuracy")

#X = ml_Analyzer.X[:,0:10]
#scaler = preprocessing.StandardScaler().fit(X)
#X = scaler.transform(X)
#gsRes.fit(X,ml_Analyzer.Y)

ml_Analyzer.classification_model_wLOOCV(model,10)