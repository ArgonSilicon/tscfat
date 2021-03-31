#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:02:27 2020

@author: arsii

Calculate a fluctuation intensity F for given timeseries. F is sensitive to 
amplitude and frequency changes in time signal. For the reference:
Schiepek, Günter, and Guido Strunk. "The identification of critical 
fluctuations and phase transitions in short term and coarse-grained time 
series—a method for the real-time monitoring of human change processes." 
Biological cybernetics 102.3 (2010): 197-207.  

"""

import numpy as np

def fluctuation_intensity(y,scale,window):
    """ Calculate fluctuation intensity for the given time series.
    
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
    F : float
        Calculated fluctuation intensity.

    """
        
    assert isinstance(y,np.ndarray), "Given time series is not a numpy array."
    assert isinstance(scale, int), "Given scale is not an integer."
    assert isinstance(window, int), "Given window length is not an integer."
    assert scale > 0, "Given scale is negative."
    assert (0 < window <= len(y)), "Improper window length."
    
    # scale
    s = scale
    # max fluctuations
    m = window - 1
    
    y = np.diff(y)
    y = np.append(y,0)
    #print(y)
    
    # intialize variables
    l = 1
    diff = 0
    diff_arr= []
    
    for i in range(window-1):
        #print("i: ",i)
        
        if np.sign(y[i]) == np.sign(y[i+1]): # continues growing / decreasing
            #print("continue")
            
            # add difference and length
            diff += y[i]
            l += 1
        
        else: # change of sign
            #print("stop")
            
            # add difference and append value
            diff += y[i]
            diff_arr.append(abs(diff/l))
            
            # reset variables
            diff = 0
            l = 1
    
    # Calculate fluctuation intensity
    F = sum(diff_arr) / (s*m)
    return F




