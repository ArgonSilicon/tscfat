# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:29:57 2020

@author: arsii
"""

from tslearn.clustering import TimeSeriesKMeans
import numpy as np
import pytest

def Cluster_timeseries(ts, n=3, mi=5, mib=5, rs=0):
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
    
   return labels


def test_Cluster_timeseries():
    from tslearn.clustering import TimeSeriesKMeans
    from tslearn.generators import random_walks
    
    X = random_walks(n_ts=50, sz=32, d=1)
    
    km_dba = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=5,
                              max_iter_barycenter=5,
                              random_state=0).fit(X)
 
    assert km_dba is not None


