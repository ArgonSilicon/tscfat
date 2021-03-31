#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:57:14 2020

@author: arsii

Calculate a distribution degree D for given timeseries. D measures the 
scattering of the time series values within the range of possible values.
For the reference:
Schiepek, Günter, and Guido Strunk. "The identification of critical 
fluctuations and phase transitions in short term and coarse-grained time 
series—a method for the real-time monitoring of human change processes." 
Biological cybernetics 102.3 (2010): 197-207.  
  
"""

import numpy as np

def distribution_degree(y,scale,window):
    """ Calculate distribution degree for given time series.

    Parameters
    ----------
    y : numpy array
        A Time series
    scale : int
        Flutuation scale: abs(max value - min value)
    window : int
        A window for calculation

    Returns
    -------
    D : float
        Calculated distribution degree.

    """
    
    assert isinstance(y, np.ndarray), "Given time series is not a numpy array."
    assert isinstance(scale, int), "Given scale is not an integer."
    assert isinstance(window, int), "Given window length is not an integer."
    assert scale > 0, "Given scale is negative."
    assert (0 < window <= len(y)), "Improper window length."
    
    s = scale
    m = window -1
    interval = s / m
    x = np.sort(y)
    y = np.array([interval*i for i in range(1,m+2)])
    sum_ab = 0
    store = 0
    
    # TODO! Time complexity is too high
    
    # calculate aberration
    for c in range(0,window-1): #0 - 6
        #print("c: ",c)
        for d in range((c+1),window): # (c+1) - 7
            #print("d: ",d)
            for a in range(c,(d)):
                #print("a: ",a)
                store += d - a
                delta_x = x[a+1:d+1] - x[a]
                delta_y = y[a+1:d+1] - y[a]
                delta = delta_y - delta_x
                ab = delta*np.heaviside(delta,0) / 1
                sum_ab += np.sum(ab)
    
    D =  1 - sum_ab / (store*2)               
    
    return D 


