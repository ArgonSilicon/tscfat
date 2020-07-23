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

def grouped_histograms(timeseries,
                       title,
                       xlabel,
                       ylabel,
                       savepath = False,
                       savename = False,
                       ):
    """
    

    Parameters
    ----------
    timeseries : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    xlabel : TYPE
        DESCRIPTION.
    ylabel : TYPE
        DESCRIPTION.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
    savename : TYPE, optional
        DESCRIPTION. The default is False.
     : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    title = "Distributions by the groups: " + title
    
    fig1 = plt.figure(figsize=(24,12))
    
    plt.suptitle(title,y=0.9,fontsize=20)
          
    for ind, val in zip(timeseries.index,timeseries.values): 
        plt.subplot(4,6,(ind+1))
        plt.hist(val,density=True,label=("hour: {}\n mean: {:.2f}".format(ind,np.mean(val))))
        plt.axvline(np.mean(val), color='r', linestyle='dashed', linewidth=2)
        if ind >= 18:
            plt.xlabel(xlabel)
        if ind%6 == 0:
            plt.ylabel(ylabel)
        plt.legend(loc='upper left')
    
    if not all((savename,savepath)):
        plt.show()

    elif all((savename,savepath)):

        assert isinstance(savename,str), "Invalid savename type."
        savename = savename + "_group_distribution"
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
        
    averages = [np.mean(val) for val in timeseries.values]
    
    fig2 = plt.figure(figsize=(14,7))
    plt.bar(timeseries.index,averages)
    plt.title(title +"_averages")
    plt.xlabel('Time / Hours')
    plt.ylabel('Percentage')
    plt.ylim(0,100)
    
    if not all((savename,savepath)):
        plt.show()

    elif all((savename,savepath)):

        assert isinstance(savename,str), "Invalid savename type."
        savename = savename + "_group_averages"
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")


def plot_differences(timeseries,
                     column_name,
                     title,
                     xlab,
                     ylab,
                     savepath = False,
                     savename = False,
                     ):
    """
    

    Parameters
    ----------
    timeseries : TYPE
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
     : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    timeseries_diff = timeseries.diff()
    stdev = timeseries_diff.std()
    print(stdev)
    #print(timeseries_diff)
    lowest = timeseries_diff[column_name].nsmallest(5, keep='all')
    
    fig = plt.figure(figsize=(15,10))
    timeseries_diff.plot()
    #plt.axvline(x=stdev,color='r')
    #plt.axvline(x=-stdev,color='r')
    plt.title(title,fontsize=16)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xticks(rotation=45)
    
    if not all((savename,savepath)):
        plt.show()

    elif all((savename,savepath)):

        assert isinstance(savename,str), "Invalid savename type."
        savename = savename + "_difference"
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
    
    return lowest

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