#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:29:57 2020

@author: arsii
"""

from tslearn.clustering import TimeSeriesKMeans
import matplotlib.pyplot as plt
import numpy as np
from Source.Utils.plot_decorator import plot_decorator
import pytest

@plot_decorator
def _plot_clusters(clusters,title,xlab="Timepoint",ylab="Cluster",savename = False, savepath = False, test=False):
    """
    Plot a scatterplot showing the clusters.

    Parameters
    ----------
    clusters : numpy array
        An array showing the corresponding clusters for the time series.
    title : str
        The plot title
    xlab : str, optional
        Plot x-label . The default is "Timepoint".
    ylab : str, optional
        Plot y-label The default is "Cluster".
    savename : Path object, optional
        Figure save name. The default is False.

    Returns
    -------
    None.

    """
    assert isinstance(clusters, np.ndarray), "Given Time series is not a numpy array."
    
    fig = plt.figure(figsize=(10,10))
    
    plt.plot(clusters,'o:')
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
    return fig
    
    
    

def cluster_timeseries(ts, FIGNAME, FIGPATH, title="Clustered timeseries", n=3, mi=5, mib=5, rs=0):
   """
    Parameters
    ----------
    ts : TYPE
        DESCRIPTION.
    n : TYPE, optional
        DESCRIPTION. The default is 3.
    mi : TYPE, optional
        DESCRIPTION. The default is 5.
    mib : TYPE, optional
        DESCRIPTION. The default is 5.
    rs : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    labels : TYPE
        DESCRIPTION.

    """
    
   assert isinstance(ts,np.ndarray), "Timeseries array type is not np.ndarray."
   assert ts.ndim == 2, "Timeseries array dimensions is not equal to 2"
    
    
   km = TimeSeriesKMeans(n_clusters = n, 
                          metric = "dtw", 
                          max_iter= mi,
                          max_iter_barycenter = mib,
                          random_state = rs).fit(ts)
    
   labels = km.labels_
   
   _plot_clusters(labels,title=title,xlab="Timepoint",ylab="Cluster",savename = FIGNAME, savepath = FIGPATH,test=False)

   return labels


def test_cluster_timeseries():
    import numpy as np

    sample = np.array([[1,1,1,2,2,2],[2,2,2,3,3,3],[1,2,3,4,5,6],[4,5,6,7,8,9]],np.int32)
    clusters = cluster_timeseries(sample, False, False, title="Clustered timeseries", n=2, mi=5, mib=5, rs=0)
    np.testing.assert_array_equal(clusters,np.array([0,0,1,1])), "Clusters are not correctly assigned."
  

