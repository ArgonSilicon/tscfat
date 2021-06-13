#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:45:10 2020

@author: arsii

Calculate rolling windows statistics for the given time series and plot them.

The following are calculated using rolling window lenght(n):
    1) Average
    2) Variance
    3) Autocorrelation
    4) Mean square of successive differences (MSDD)
    5) Probability of acte change (PAC)

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#from arma_model import autocorr
from tscfat.Analysis.fluctuation_intensity import fluctuation_intensity
from scipy.stats import entropy
#import nolds
from tscfat.Utils.plot_decorator import plot_decorator
from datetime import datetime
from matplotlib.dates import date2num

#TODO! why pandas dataframe is required!!!!
#TODO! fix doi!!!
#TODO! select reasonable features to plot!!!

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
                       doi = None,
                       savename = False,
                       savepath = False,
                       test = False):
    """ Calculate and plot several rolling statistics.

    Parameters
    ----------
    ts : pandas dataframe
        A dataframe containing time as index and one column of data
    w : int
        Rolling statistics window size
    doi : tuple 
        A tuple containing tuples of dates. The default is None. 
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
    # TODO! assert doi!!!
    
    
    variance = ts.rolling(window = w).var()
    autocorrelation = ts.rolling(window = w).apply(_autocorr)
    mean = ts.rolling(window = w).mean() 
    skew = ts.rolling(window = w).skew()
    kurt = ts.rolling(window = w).kurt()
    flu_int = ts.rolling(window = w).apply(lambda x: fluctuation_intensity(x.values,100,w))#,args=(100,w))
    ent = ts.rolling(window = w).apply(entropy)
    #ent = ts.rolling(window = w).apply(nolds.sampen)
    
    var1 = ts.diff(1).fillna(0).rolling(window = w).var()
    var2 = ts.diff(1).diff(7).fillna(0).rolling(window = w).var()
    var3 = ts.diff(1).diff(7).diff(28).fillna(0).rolling(window = w).var()
    
    ac1 = ts.diff(1).fillna(0).rolling(window = w).apply(_autocorr)
    ac2 = ts.diff(1).diff(7).fillna(0).rolling(window = w).apply(_autocorr)
    ac3 = ts.diff(1).diff(7).diff(28).fillna(0).rolling(window = w).apply(_autocorr)
    
    #fig,ax = plt.subplots(4,2,figsize=(20,20))
    fig,ax = plt.subplots(3,2,figsize=(15,15))
    fig.suptitle("Rolling Statistics (window length: {}): {}".format(w,ts.columns[0]),fontsize=28,y=1.0)
    
    ax[0,0].plot(ts)
    ax[0,0].set_title('Original timeseries',fontsize=26)
    ax[0,0].set_xlabel('Date',fontsize=24)
    ax[0,0].set_ylabel('Value',fontsize=24)
    ax[0,0].tick_params('x', labelrotation=45)
    ax[0,0].tick_params(axis='both', labelsize=20)
    if doi is not None:
        ax[0,0].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[0,1].plot(mean)
    ax[0,1].set_title('Mean',fontsize=26)
    ax[0,1].set_xlabel('Date',fontsize=24)
    ax[0,1].set_ylabel('Value',fontsize=24)
    ax[0,1].tick_params('x', labelrotation=45)
    ax[0,1].tick_params(axis='both', labelsize=20)
    if doi is not None:
        ax[0,1].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[1,0].plot(variance)
    ax[1,0].set_title('Variance',fontsize=26)
    ax[1,0].set_xlabel('Date',fontsize=24)
    ax[1,0].set_ylabel('Value',fontsize=24)
    ax[1,0].tick_params('x', labelrotation=45)
    ax[1,0].tick_params(axis='both', labelsize=20)
    if doi is not None:
        ax[1,0].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[1,1].plot(autocorrelation)
    ax[1,1].set_title('Autocorrelation',fontsize=26)
    ax[1,1].set_xlabel('Date',fontsize=24)
    ax[1,1].set_ylabel('Value',fontsize=24)
    ax[1,1].tick_params('x', labelrotation=45)
    ax[1,1].tick_params(axis='both', labelsize=20)
    if doi is not None:
        ax[1,1].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[2,0].plot(skew)
    ax[2,0].set_title('Skewness',fontsize=26)
    ax[2,0].set_xlabel('Date',fontsize=24)
    ax[2,0].set_ylabel('Value',fontsize=24)
    ax[2,0].tick_params('x', labelrotation=45)
    ax[2,0].tick_params(axis='both', labelsize=20)
    if doi is not None:
        ax[2,0].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[2,1].plot(kurt)
    ax[2,1].set_title('Kurtosis',fontsize=26)
    ax[2,1].set_xlabel('Date',fontsize=24)
    ax[2,1].set_ylabel('Value',fontsize=24)
    ax[2,1].tick_params('x', labelrotation=45)
    ax[2,1].tick_params(axis='both', labelsize=20)
    if doi is not None:    
        ax[2,1].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    '''
    ax[3,0].plot(flu_int)
    ax[3,0].set_title('Fluctuation Intensity',fontsize=18)
    ax[3,0].set_xlabel('Date',fontsize=14)
    ax[3,0].set_ylabel('Value',fontsize=14)
    ax[3,0].tick_params('x', labelrotation=45)
    if doi is not None:
        ax[3,0].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[3,1].plot(ent)
    ax[3,1].set_title('Entropy',fontsize=18)
    ax[3,1].set_xlabel('Date',fontsize=14)
    ax[3,1].set_ylabel('Value',fontsize=14)
    ax[3,1].tick_params('x', labelrotation=45)
    if doi is not None:
        ax[3,1].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    
    ax[4,0].plot(var3)
    ax[4,0].set_title('Variance, diff(1,7,28)',fontsize=16)
    ax[4,0].set_xlabel('Date')
    ax[4,0].set_ylabel('Value')
    ax[4,0].tick_params('x', labelrotation=45)
    if doi is not None:
        ax[4,0].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[4,1].plot(ac3)
    ax[4,1].set_title('Autocorrelation, diff(1,7,28)',fontsize=16)
    ax[4,1].set_xlabel('Date')
    ax[4,1].set_ylabel('Value')
    ax[4,1].tick_params('x', labelrotation=45)
    if doi is not None:
        ax[4,1].axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    '''
    
    plt.tight_layout(pad=1)
  
    return fig