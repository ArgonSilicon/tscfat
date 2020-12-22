# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:29:57 2020

@author: arsii
"""

from tslearn.clustering import TimeSeriesKMeans
import matplotlib.pyplot as plt
import numpy as np
import pytest

def __Plot_clusters(clusters,title,xlab="Timepoint",ylab="Cluster",savename = False, savepath = False):
    """
    

    Parameters
    ----------
    clusters : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    xlab : TYPE, optional
        DESCRIPTION. The default is "Timepoint".
    ylab : TYPE, optional
        DESCRIPTION. The default is "Cluster".
    savename : TYPE, optional
        DESCRIPTION. The default is False.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

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
    
    if not savename and not savepath:
        plt.show()
        
    elif savename and savepath:
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")

def Cluster_timeseries(ts, FIGNAME, FIGPATH, title="Clustered timeseries", n=3, mi=5, mib=5, rs=0):
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
   
   __Plot_clusters(labels,title=title,xlab="Timepoint",ylab="Cluster",savename = FIGNAME, savepath = FIGPATH)
    
   return labels


def test_Cluster_timeseries():
    from tslearn.clustering import TimeSeriesKMeans
    from tslearn.generators import random_walks
    
    X = random_walks(n_ts=50, sz=32, d=1)
    
    km_dba = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=5,
                              max_iter_barycenter=5,
                              random_state=0).fit(X)
 
    assert km_dba is not None


