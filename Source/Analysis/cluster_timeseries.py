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
from datetime import datetime
from matplotlib.dates import date2num
from collections import Counter

@plot_decorator
def _plot_clusters(clusters,title,xlab="Timepoint",ylab="Cluster",savename = False, savepath = False, highlight = False, test=False):
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
    
    plt.plot(clusters +1 ,'o:')
    if highlight:
        plt.axvspan(highlight[0],highlight[1],ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.yticks(np.arange(1,6))
    
    return fig

@plot_decorator
def _plot_cluster_averages(data, clusters, n, title, xlab = "Time (hour)", ylab = None, ylim_ = None, savename = False, savepath = False, test=False):
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
    
    l = clusters.shape[0]
    filt = np.zeros((n,l)).astype(bool)
    
    for i in range(n):
        filt[i,:] = clusters == i
            
    fig,ax = plt.subplots(n,1,figsize=(10,20))
    fig.suptitle(title + '\n cluster averages', fontsize = 20, y=1)
    
    for i in range(n):
        ax[i].plot(np.mean(data[filt[i]], axis = 0))
        ax[i].set_title('Cluster {} average'.format(i))
        ax[i].set(xlabel = xlab, ylabel = ylab) 
        if ylim_:
            ax[i].set(ylim = ylim_)
        
    fig.tight_layout(pad=1.0)
                      
    return fig    
    

def cluster_timeseries(ts, FIGNAME, FIGPATH, title="Clustered timeseries", n=3, mi=5, mib=5, rs=0, metric = "dtw", highlight = None, ylim_ = None):
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
    metric : TYPE. optional
        DESCRIPTION. The default is "dtw".
    highlight : TYPE, optional
        DESCRIPTION. The default is None
    highlight : TYPE, optional
        DESCRIPTION. The default is None
        
    Returns
    -------
    labels : TYPE
        DESCRIPTION.

    """
    
   assert isinstance(ts,np.ndarray), "Timeseries array type is not np.ndarray."
   assert ts.ndim == 2, "Timeseries array dimensions is not equal to 2"
    
    
   km = TimeSeriesKMeans(n_clusters = n, 
                          metric = metric, 
                          max_iter = mi,
                          max_iter_barycenter = mib,
                          random_state = rs,
                          ).fit(ts)
    
   labels = km.labels_
   
   #TODO fix x-axis
   
   _plot_clusters(labels, 
                  title=title, 
                  xlab="Timepoint", 
                  ylab="Cluster", 
                  savename = FIGNAME, 
                  savepath = FIGPATH, 
                  highlight = highlight, 
                  test = False)
   if FIGNAME:
       FIGNAME = FIGNAME + '_cluster_averages'
       
   _plot_cluster_averages(ts, 
                          labels, 
                          n, 
                          title, 
                          xlab = "Time (hour)", 
                          ylab = None, 
                          ylim_ = ylim_,
                          savename = FIGNAME, 
                          savepath = FIGPATH,
                          test = False)
   
   return labels


def test_cluster_timeseries():
    import numpy as np

    sample = np.array([[1,1,1,2,2,2],[2,2,2,3,3,3],[1,2,3,4,5,6],[4,5,6,7,8,9]],np.int32)
    clusters = cluster_timeseries(sample, False, False, title="Clustered timeseries", n=2, mi=5, mib=5, rs=0)
    np.testing.assert_array_equal(clusters,np.array([0,0,1,1])), "Clusters are not correctly assigned."
  

