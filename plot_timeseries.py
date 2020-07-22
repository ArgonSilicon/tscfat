#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 14:56:03 2020

@author: arsi
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import seaborn as sns
from interpolate_missing import interpolate_missing
from arma import arma, autocorr
from scipy.signal import find_peaks

def show_features(timeseries,               
                  title,
                  xlab,
                  ylab,
                  window = 7,
                  mp = 1,
                  cl = "right",
                  interpolation = False,
                  savepath = False,
                  savename = False,
                  ):
    
    # TODO: write assertions here
    # TODO: write docstrings
    
    features_to_calculate = [np.var]
    
    if interpolation:
        
        assert isinstance(interpolation,str), "Interpolation type is: {}, not str".format(type(interpolation))
        
        timeseries, missing_mask = interpolate_missing(timeseries,interpolation)
    
    #print(timeseries)
    
    rolling_ts = timeseries.rolling(window,
                                    min_periods = 1, 
                                    closed = 'right')
    
   
    features = rolling_ts.aggregate(features_to_calculate)
    features['autocorr'] = timeseries.rolling(window).apply(autocorr)
    
    
    #%%
    
    title = "Extracted features" + title
    
    fig = plt.figure(figsize=(15,15))
    
    plt.suptitle(title,fontsize=20)
    
    plt.subplot(2,1,1)
    features.iloc[:,0].plot()
    plt.title('STD',fontsize=16)
    plt.xlabel('Time')
    plt.ylabel("Value")
    plt.xticks(rotation=45)
                
    plt.subplot(2,1,2)
    features.iloc[:,1].plot()
    plt.title('Autocorrelation',fontsize=16)
    plt.xlabel('Time')
    plt.ylabel("Value")
    plt.xticks(rotation=45)
     
    fig.tight_layout(pad=4.0)
    plt.grid(True)
    plt.legend()
    
    if not all((savename,savepath)):
        plt.show()

    elif all((savename,savepath)):

        assert isinstance(savename,str), "Invalid savename type."
        savename2 = savename + "_features"
        
        if savepath.exists():
            with open(savepath / (savename2 + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.") 

    
def show_timeseries_scatter(series,
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
    -------    #%% show features
     #%% Plot timeseries and save figure
    FIGNAME = "timeseries_scatter_" + key
    show_timeseries_scatter(pd_series,"Conversation / hourly binned seconds","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_line_" + key
    show_timeseries_line(pd_series,"Conversation / hourly binned seconds","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_features_" + key
    show_features(pd_series,"Conversation","xlab","ylab",48,1,'right',False,FIGPATH,FIGNAME)
    None.

    """
    
    # TODO: Insert assertions!
    # TODO: add legend
    
    plt.figure(figsize=(15,15))
    #plt.scatter(x_name, y_name)
    series.plot(style='.')
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