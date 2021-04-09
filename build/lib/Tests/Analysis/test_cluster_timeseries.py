#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:08 2021

@author: arsii

Test function for time series clustering.

"""

import numpy as np

from tscfat.Analysis.cluster_timeseries import cluster_timeseries, _plot_clusters

class TestClusterTimeseries(object):
    
    def test_cluster_timeseries(self):
        """ Test that the clusters are correctly assigned.
        

        Returns
        -------
        None.

        """
   
        sample = np.array([[1,1,1,2,2,2],[2,2,2,3,3,3],[1,2,3,4,5,6],[4,5,6,7,8,9]],np.int32)
        clusters = cluster_timeseries(sample, False, False, title="Clustered timeseries", n=2, mi=5, mib=5, rs=0)
        np.testing.assert_array_equal(clusters,np.array([0,0,1,1])), "Clusters are not correctly assigned."
        
    def test_plot_clusters(self):
        """ Test that the _plot_clusters function returns something.
        

        Returns
        -------
        None.

        """
      
        sample = np.array([1,1,1,2,2,2,3,3,3])
        res = _plot_clusters(sample, title="test", xlab="Timepoint", ylab="Cluster", savename = False, savepath = False, test = True)
        assert res is not None