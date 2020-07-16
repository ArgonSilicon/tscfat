#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:36:18 2020

@author: arsii

Calculate ARMA model or autocorrelation for given timeseries.

"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARMA


def autocorr(series, t=1):
    """ Calculate autocorrelation for given timeseries
    

    Parameters
    ----------
    series : pandas series or numpy array
        Timeseries for autocorrelation 
    t : int (default=1)
        Autocorrelation lag

    Returns
    -------
    cc: float
        autocorrelation coefficient (lag = 1)

    """
    
    # TODO: insert assertions
    
    timeseries = series.values.reshape(-1)
    cc = np.corrcoef(np.array([timeseries[:-t], timeseries[t:]]))
    return cc[0][1]  


def arma(series,ar=1,ma=0):
    """ Calculate ARMA model for given timeseries.

    Parameters
    ----------
    series : pandas series or numpy array
        Timeseries for ARMA model
    ar : int (default = 1)
        ARMA model autoregression parameter
    ma : int (default = 0)
        ARMA model moving average parameter
    
    Returns
    -------
    result : ARMAResultWrapper object
        Object containing the ARMA results
    
    """
    
    # TODO: fix assertions
    '''
    assert isinstance(series,(pd.core.series.Series, np.ndarray), "Timeseries should be a Pandas series type or an numpy array."
    assert isinstance(ar,int), "Unit type should be int, not {}".format(type(ar))
    assert isinstance(ma,int), "Unit type should be int, not {}".format(type(ma))
    '''
    #series.index = series.index.to_period('H')
    model = ARMA(series, order=(ar,ma))
    result = model.fit()
    return result.params[1]