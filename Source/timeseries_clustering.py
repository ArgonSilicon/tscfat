# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:29:57 2020

@author: arsii
"""


from tslearn.clustering import TimeSeriesKMeans
from tslearn.generators import random_walks
from tslearn.utils import to_time_series_dataset
import numpy as np
import matplotlib.pyplot as plt
import pytest
from setup import setup_np, setup_pd


def Cluster_timeseries(ts,n=3,mi=5, mib=5, rs = 0):
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
    '''
    test_argument = np.array([[1382.0, 390167.0]])
    # Store information about raised ValueError in exc_info
    with pytest.raises(ValueError) as exc_info:
      split_into_training_and_testing_sets(test_argument)
    expected_error_msg = "Argument data_array must have at least 2 rows, it actually has just 1"
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    '''
    pass
