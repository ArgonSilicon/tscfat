#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:40:46 2020

@author: arsi

Calculate STL decomposition for given time series and plot the components.
The decomposition is based on statsmodels STL decomposition. Full reference:
https://www.statsmodels.org/devel/generated/statsmodels.tsa.seasonal.STL.html

"""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from tscfat.Utils.plot_decorator import plot_decorator
from datetime import datetime
from matplotlib.dates import date2num

#TODO! = fix the xlabels 

@plot_decorator
def _plot_decomposition(Result,
                        title,
                        savepath = False,
                        savename = False,
                        ylabel = "Value",
                        xlabel  = "Date",
                        dates = False,
                        test = False,
                        doi = None,
                        ):
    
    #TODO fix docstrings
    
    """ Plot the decomposed time series.

    Parameters
    ----------
    Result : statsmodels.tsa.seasonal.DecomposeResult object
        Object containing the decomposition results    
    title : str
        Figure title.
    savepath : Path object, optional
        Figure save path The default is False.
    savename : str, optional
        Figure save name. The default is False.
    ylabel : str, optional
        Figure ylabel. The default is "Battery Level (%)".
    xlabel : str, optional
        Figure xlabel. The default is "Date".
    dates : array, optional
        List of daytes to be highlighted in the figure. The default is False.
    doi   :
        

    Raises
    ------
    Exception
        - savepath does not exist
        - savename or path was not given in correct format

    Returns
    -------
    None.

    """
    
    
    fig, ax = plt.subplots(4,1,figsize=(15,17))
    
    plt.suptitle(title, fontsize=42, y=1)
    
    ax[0].plot(Result.observed)
    #Result.observed.plot(ax=ax[0])
    if doi is not None:
        #ax[0].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")    
        ax[0].axvspan(doi[0], doi[1],facecolor="yellow",alpha=0.13,label="Days of interest")
        
    ax[0].set_title('Observations',fontsize=38)
    ax[0].tick_params(axis='both', labelsize=24)
    ax[0].set_ylabel(ylabel,fontsize=32)
    ax[0].set_xlabel(xlabel,fontsize=32)
    
    ax[1].plot(Result.trend)
    #Result.trend.plot(ax=ax[1])
    if doi is not None:
        #ax[1].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")
        ax[1].axvspan(doi[0], doi[1],facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[1].tick_params(axis='both', labelsize=24)
    ax[1].set_title('Trend',fontsize=38)
    ax[1].set_ylabel(ylabel,fontsize=32)
    ax[1].set_xlabel(xlabel,fontsize=32)
    
    ax[2].plot(Result.seasonal)
    #Result.seasonal.plot(ax=ax[2])
    if doi is not None:
        #ax[2].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")
        ax[2].axvspan(doi[0], doi[1],facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[2].tick_params(axis='both', labelsize=24)
    ax[2].set_title('Seasonal',fontsize=38)
    ax[2].set_ylabel(ylabel,fontsize=32)
    ax[2].set_xlabel(xlabel,fontsize=32)
    
    ax[3].plot(Result.resid)
    #Result.resid.plot(ax=ax[3])
    if doi is not None:
        #ax[3].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")
        ax[3].axvspan(doi[0], doi[1],facecolor="yellow",alpha=0.13,label="Days of interest")
    
    ax[3].tick_params(axis='both', labelsize=24)
    ax[3].set_title('Residuals',fontsize=38)
    ax[3].set_ylabel(ylabel,fontsize=32)
    ax[3].set_xlabel(xlabel,fontsize=32)
    
    '''
    fig1 = plt.figure(figsize=(10,10))
    
    plt.suptitle(title, fontsize=22, y=0.95)
    
    plt.subplot(4,1,1)
    plt.plot(Result.observed)
    plt.title('Observations',fontsize=26)
    if type(dates) != bool:       
        for d in dates:
            plt.axvline(x=d,linestyle =":", color ='black')
    if doi is not None:
        plt.axvspan(doi[0], doi[1], ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    plt.ylabel(ylabel,fontsize=14)
    plt.xlabel(xlabel,fontsize=14)
    
                
    plt.subplot(4,1,2)
    plt.plot(Result.trend)
    plt.title('Trend',fontsize=18)
    if type(dates) != bool:       
        for d in dates:
            plt.axvline(x=d,linestyle =":", color ='black')
    plt.ylabel(ylabel,fontsize=14)
    plt.xlabel(xlabel,fontsize=14)
     
    plt.subplot(4,1,3)
    plt.plot(Result.seasonal)
    if type(dates) != bool:       
        for d in dates:
            plt.axvline(x=d,linestyle =":", color ='black')
    plt.title('Seasonal',fontsize=18)
    plt.ylabel(ylabel,fontsize=14)
    plt.xlabel(xlabel,fontsize=14)
     
    plt.subplot(4,1,4)
    plt.plot(Result.resid)
    if type(dates) != bool:       
        for d in dates:
            plt.axvline(x=d,linestyle =":", color ='black')
    plt.title('Residuals',fontsize=18)
    plt.ylabel(ylabel,fontsize=14)
    plt.xlabel(xlabel,fontsize=14)
    '''
    fig.tight_layout(pad=1)
    
    return fig

def STL_decomposition(series,
                      title,
                      test = False,
                      savepath = False,
                      savename = False,
                      ylabel = "Battery Level (%)",
                      xlabel  = "Date",
                      dates = False,
                      doi = None,
                      ):
    """ Decompose timeseries into Model, Trend, Seasonal and Residual parts.
    Plot the components and their distributions. Optionally save the figure.
    
        
    Parameters
    ----------
    series : Numpy ndarray
        Time series to be decomposed
    title : str
        Figure title.
    savepath : Path object, optional
        Figure save path The default is False.
    savename : str, optional
        Figure save name. The default is False.
    ylabel : str, optional
        Figure ylabel. The default is "Battery Level (%)".
    xlabel : str, optional
        Figure xlabel. The default is "Date".
    dates : array, optional
        List of daytes to be highlighted in the figure. The default is False.

    Raises
    ------
    Exception
        - given series is not a numpy array.
        

    Returns
    -------
    Result : statsmodels.tsa.seasonal.DecomposeResult object
        Object containing the decomposition results.

    """
    assert isinstance(series, np.ndarray), "Series is not a numpy array."
    
    Result = STL(series, 
                 period=24, 
                 seasonal=7, 
                 trend=None, 
                 low_pass=None,
                 seasonal_deg=0, 
                 trend_deg=0, 
                 low_pass_deg=0, 
                 robust=False,
                 seasonal_jump=1, 
                 trend_jump=1, 
                 low_pass_jump=1).fit()

    if test == False:
        _plot_decomposition(Result,
                            title,
                            savepath = savepath,
                            savename = savename,
                            ylabel = "Value",
                            xlabel  = "Day",
                            dates = False,
                            test = False,
                            doi = doi,
                            )
        
    return Result
    

        
