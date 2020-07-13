#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:40:46 2020

@author: arsi
"""
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose,STL


def Decompose_timeseries(series,
                         model = 'multiplicative',
                         plot = False):
    """
    Decompose timeseries into Model, Trend, Seasonal and Residual parts.

    Parameters
    ----------
    series : TYPE
        DESCRIPTION.
    model : TYPE, optional
        DESCRIPTION. The default is 'multiplicative'.
    plot : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    result : TYPE
        DESCRIPTION.

    """
    # TODO some asserts
    # TODO finish docstrings
    # TODO additional arguments?
    
    try:
        if model == 'multiplicative':
            result = seasonal_decompose(series, model='multiplicative')
            
        elif model == 'additive':
            result = seasonal_decompose(series, model='additive')
         
        elif model == "STL":
            result = STL(series).fit()
                        
    except ValueError:
        print("No valid model (multiplicative,additive or STL) was given")
    
    if plot:
            plt.figure(figsize=(20,20))
            plt.title('Timeseries decomposition')
            plt.xticks(rotation=45)
            result.plot()
            plt.show()
            
    return result
    