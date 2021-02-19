#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:45:10 2020

@author: arsii

Calculate rolling windows statistic for the given time series and plot them.

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#from arma_model import autocorr
from Source.Analysis.fluctuation_intensity import fluctuation_intensity
from scipy.stats import entropy
import nolds
import pytest
from Source.Utils.plot_decorator import plot_decorator

def _autocorr(series, t=1):
    """ Calculate autocorrelation for given timeseries
    

    Parameters
    ----------
    series : pandas series or numpy array
        Timeseries for autocorrelation 
    t : int (default=1)
        Autocorrelation lag
        
    Raises
    ------
    Exception
        - given time series is not a pandas series
        - given windows size is not an integer
        
    Returns
    -------
    cc: float
        autocorrelation coefficient (lag = 1)

    """
    
    assert isinstance(series, pd.Series), 'Given time series is not an pandas series'
    assert isinstance(t,int), 'Given lag is not an integer'
    
    timeseries = series.values.reshape(-1)
    cc = np.corrcoef(np.array([timeseries[:-t], timeseries[t:]]))
    return cc[0][1]

@plot_decorator
def rolling_statistics(ts,
                       w,
                       savename = False,
                       savepath = False,
                       test = False):
    """
    Calculate and plot several rolling statistics.

    Parameters
    ----------
    ts : pandas dataframe
        A dataframe containing time as index and one column of data
    w : int
        Rolling statistics window size
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where plot is to be saved. Path has to exist before calling this 
        function.
    test : Boolean, optional
        Flag for test function. The default is False.
        
    Raises
    ------
    Exception
        - given time series is not a pandas dataframe
        - given windows size is not an integer
        - given window length is larger than the time series length

    Returns
    -------
        None or matplotlib.pyplot figure is test if True.

    """
    
    assert isinstance(ts,pd.DataFrame), "Timeseries is not a pandas dataframe."
    assert isinstance(w,int), "Window size is not an integer."
    assert (w <= ts.shape[0]), "Window length is larger than the time series length."
    
    variance = ts.rolling(window = w).var()
    autocorrelation = ts.rolling(window = w).apply(_autocorr)
    mean = ts.rolling(window = w).mean() 
    skew = ts.rolling(window = w).skew()
    kurt = ts.rolling(window = w).kurt()
    flu_int = ts.rolling(window = w).apply(lambda x: fluctuation_intensity(x.values,100,w))#,args=(100,w))
    ent = ts.rolling(window = w).apply(entropy)
    #ent = ts.rolling(window = w).apply(nolds.sampen)
    
    
    fig,ax = plt.subplots(4,2,figsize=(10,10))
    fig.suptitle("Rolling Statistics {}".format(ts.columns[0]),fontsize=20,y=1.0)
    
    ax[0,0].plot(ts)
    ax[0,0].set_title('Original timeseries',fontsize=16)
    ax[0,0].set_xlabel('Date')
    ax[0,0].set_ylabel('Value')
    ax[0,0].tick_params('x', labelrotation=45)
    
    ax[0,1].plot(mean)
    ax[0,1].set_title('Mean',fontsize=16)
    ax[0,1].set_xlabel('Date')
    ax[0,1].set_ylabel('Value')
    ax[0,1].tick_params('x', labelrotation=45)
    
    ax[1,0].plot(variance)
    ax[1,0].set_title('Variance',fontsize=16)
    ax[1,0].set_xlabel('Date')
    ax[1,0].set_ylabel('Value')
    ax[1,0].tick_params('x', labelrotation=45)
    
    ax[1,1].plot(autocorrelation)
    ax[1,1].set_title('Autocorrelation',fontsize=16)
    ax[1,1].set_xlabel('Date')
    ax[1,1].set_ylabel('Value')
    ax[1,1].tick_params('x', labelrotation=45)
    
    ax[2,0].plot(skew)
    ax[2,0].set_title('Skewness',fontsize=16)
    ax[2,0].set_xlabel('Date')
    ax[2,0].set_ylabel('Value')
    ax[2,0].tick_params('x', labelrotation=45)
    
    ax[2,1].plot(kurt)
    ax[2,1].set_title('Kurtosis',fontsize=16)
    ax[2,1].set_xlabel('Date')
    ax[2,1].set_ylabel('Value')
    ax[2,1].tick_params('x', labelrotation=45)
    
    ax[3,0].plot(flu_int)
    ax[3,0].set_title('Fluctuation intensity',fontsize=16)
    ax[3,0].set_xlabel('Date')
    ax[3,0].set_ylabel('Value')
    ax[3,0].tick_params('x', labelrotation=45)
    
    ax[3,1].plot(ent)
    ax[3,1].set_title('Entropy',fontsize=16)
    ax[3,1].set_xlabel('Date')
    ax[3,1].set_ylabel('Value')
    ax[3,1].tick_params('x', labelrotation=45)
    
    plt.tight_layout(pad=1)
  

