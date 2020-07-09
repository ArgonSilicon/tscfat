#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 14:56:03 2020

@author: arsi
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from interpolate_missing import interpolate_missing
from arma import arma

def show_features(timeseries,               
                  title,
                  xlab,
                  ylab,
                  window = 24,
                  mp = 1,
                  cl = "right",
                  interpolation = False,
                  savepath = False,
                  savename = False,
                  ):
    
    # TODO: write assertions here
    # TODO: write docstrings
    #features_to_calculate = [np.min,np.max,np.mean,np.std] 
    features_to_calculate = [np.mean,np.std]
    
    if interpolation:
        
        assert isinstance(interpolation,str), "Interpolation type is: {}, not str".format(type(interpolation))
        
        timeseries, missing_mask = interpolate_missing(timeseries,interpolation)
    
    #print(timeseries)
    
    rolling_ts = timeseries.rolling(window, 
                                    min_periods = mp, 
                                    closed = cl)
    
    #print(rolling_ts)
    features = rolling_ts.aggregate(features_to_calculate)
    
    #print(features)
    
    # features['ar_1'] = (timeseries.iloc[:,0]).rolling(window).apply(arma)
    # plt.subplots(figsize=(10,10))
    n = timeseries.shape[0]
    timeseries_noise = timeseries + 0.00001*np.random.rand(n,)
    features['ar_1'] = timeseries_noise.rolling(48).apply(arma)
    #features['Observations'] = timeseries.values
    #plt.plot(features['ar_1'], label = "Autoregression_1")
    #plt.plot(features['screen_status']['std'],label="STD")
    
    
    features.plot()
    plt.title(title)
    plt.xlabel('Day')
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def show_timeseries_scatter(x_name,
                    y_name,
                    title,
                    xlab,
                    ylab,
                    savepath = False, 
                    savename = False):
    
    #  TODO: fill docstrings!
    
    """ Timeseries docstrings go here 
    
   
    
    Parameters
    ----------
    x_name : TYPE
        DESCRIPTION.
    y_name : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    xlab : TYPE
        DESCRIPTION.
    ylab : TYPE
        DESCRIPTION.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
    savename : TYPE, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    # TODO: Insert assertions!
    
    plt.figure(figsize=(15,15))
    plt.scatter(x_name, y_name)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xticks(rotation=45)
    
    if not all((savename,savepath)):
        plt.show()
        
    elif all((savename,savepath)):
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
        
def show_timeseries_line(series,
                         title,
                         xlab,
                         ylab,
                         savepath = False, 
                         savename = False):
    
    #  TODO: fill docstrings!
    
    """ Timeseries docstrings go here 
    
   
    
    Parameters
    ----------
    x_name : TYPE
        DESCRIPTION.
    y_name : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    xlab : TYPE
        DESCRIPTION.
    ylab : TYPE
        DESCRIPTION.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
    savename : TYPE, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    # TODO: Insert assertions!
    
    plt.figure(figsize=(15,15))
    series.plot()
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xticks(rotation=45)
    
    if not all((savename,savepath)):
        plt.show()
        
    elif all((savename,savepath)):
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")       
        
if __name__ == "__main__":
    pass