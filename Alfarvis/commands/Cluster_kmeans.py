#!/usr/bin/env python
"""
Cluster using kmeans
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject, splitPattern,
                                        findNumbers, searchDateTime)
from .abstract_command import AbstractCommand
from .argument import Argument
from Alfarvis.printers import Printer, TablePrinter
from Alfarvis.windows import Window
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from .Stat_Container import StatContainer
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from Alfarvis.Toolboxes.DataGuru import DataGuru
from sklearn import preprocessing
from .Viz_Container import VizContainer


class Cluster_kmeans(AbstractCommand):
    """
    Cluster using kmeans
    """

    def briefDescription(self):
        return "cluster data using kmeans"

    def commandType(self):
        return AbstractCommand.CommandType.MachineLearning
    
    def __init__(self, condition=["cluster"]):
        self._condition = condition

    def commandTags(self):
        """
        Tags to identify the clustering command
        """
        return self._condition + ["kmeans","k means"]

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the kmeans command
        """
        
        return [Argument(keyword="array_datas", optional=True,
                         argument_type=DataType.array, number=-1, fill_from_cache=False), 
                Argument(keyword="data_frame", optional=True,
                         argument_type=DataType.csv, number=1, fill_from_cache=False),
                         Argument(keyword="target", optional=False,
                         argument_type=DataType.user_conversation)]

    def evaluate(self, data_frame, array_datas,target):
        """
        Run clustering on a dataset of multiple arrays

        """
        
        # Get the data frame        
        if data_frame is not None:
            df = data_frame.data
            df = DataGuru.convertStrCols_toNumeric(df)
            cname = data_frame.name
        elif array_datas is not None:
            command_status, df, kl1, cname = DataGuru.transformArray_to_dataFrame(
                array_datas,useCategorical=True)
            if command_status == CommandStatus.Error:
                return ResultObject(None, None, None, CommandStatus.Error)
        else: 
            Printer.Print("Please provide data frame or arrays to analyze")
            return ResultObject(None, None, None, CommandStatus.Error)
        Y = None        
        if StatContainer.ground_truth is not None:
            df = DataGuru.removeGT(df, StatContainer.ground_truth)
            Y = StatContainer.filterGroundTruth()            
            # Remove nans:
            df, Y = DataGuru.removenan(df, Y)
        else:
            df.dropna(inplace=True)

        # Get the tsne model
        

        # Code to run the classifier
        X = df.values

        # Get a standard scaler for the extracted data X
        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        # Train the classifier
        numbers = findNumbers(target.data, 1)
        if numbers != [] and numbers[0].data > 0:
            num_clusters = int(numbers[0].data)
        else:
            num_clusters = 2  # If not specified use 2 clusters
        kY = self.performOperation(X,num_clusters)
        result_objects = []
        if StatContainer.ground_truth is not None:
            df_res = pd.DataFrame()
            df_res['ground_truth'] = Y
            df_res['clustering_result'] = kY
            df_res.pivot_table(index=df_res.columns[0], columns=df_res.columns[1], aggfunc=np.size, fill_value=0)
            win = Window.window()
            f = win.gcf()
            ax = f.add_subplot(111)
            sns.heatmap(df_res, ax=ax)
            win.show()
            if data_frame is not None:
                result_object = VizContainer.createResult(win, data_frame, ['clstr.fig'])
            else:
                result_object = VizContainer.createResult(win, array_datas, ['clstr.fig'])
            result_objects.append(result_object)
        
        result_object = ResultObject(kY, [],
                                         DataType.array,
                                         CommandStatus.Success)
        result_object.createName(
                    cname,
                    command_name = "clstr",
                    set_keyword_list=True)
        
        result_objects.append(result_object)
        return result_objects
    
    def performOperation(self,X,num_clusters):
        kmns = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
        kY = kmns.fit_predict(X)
        return kY
        
class Cluster_spectral(Cluster_kmeans):
    def __init__(self):
        super(Cluster_spectral, self).__init__(["cluster","spectral clustering","spectral"])

    def briefDescription(self):
        return "cluster using spectral clustering"

    def performOperation(self, X,num_clusters):
        kmns = SpectralClustering(n_clusters=num_clusters,  gamma=0.5, affinity='rbf', eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None, n_jobs=1)
        kY = kmns.fit_predict(X)
        return kY
    

class Cluster_hierarchical(Cluster_kmeans):
    def __init__(self):
        super(Cluster_hierarchical, self).__init__(["cluster","hierarchical clustering","hierarchical"])

    def briefDescription(self):
        return "cluster using hierarchical clustering"

    def performOperation(self, X,num_clusters):
        aggC = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
        kY = aggC.fit_predict(X)
        return kY