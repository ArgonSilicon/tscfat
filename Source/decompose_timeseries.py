#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:40:46 2020

@author: arsi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose,STL
from scipy import signal
from scipy.signal import find_peaks
from scipy.special import expit, logit
from datetime import datetime 
from setup import setup_np, setup_pd
import pytest


def plot_decomposition(Result,
                      title,
                      savepath = False,
                      savename = False,
                      ylabel = "Battery Level (%)",
                      xlabel  = "Date",
                      dates = False,
                      ):
    """
    

    Parameters
    ----------
    Result : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
    savename : TYPE, optional
        DESCRIPTION. The default is False.
    ylabel : TYPE, optional
        DESCRIPTION. The default is "Battery Level (%)".
    xlabel : TYPE, optional
        DESCRIPTION. The default is "Date".
    dates : TYPE, optional
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
    
    fig1 = plt.figure(figsize=(9.3,9.3))
    
    plt.suptitle(title,fontsize=22,y=1.05)
    
    plt.subplot(4,1,1)
    plt.plot(Result.observed)
    plt.title('Observations',fontsize=18)
    if type(dates) != bool:       
        for d in dates:
            plt.axvline(x=d,linestyle =":", color ='black')
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
    
    fig1.tight_layout(pad=2)
    
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
        
    


def STL_decomposition(series,
                      title,
                      test = False,
                      savepath = False,
                      savename = False,
                      ylabel = "Battery Level (%)",
                      xlabel  = "Date",
                      dates = False,
                      ):
    """
    STL Decompose timeseries into Model, Trend, Seasonal and Residual parts.
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
        - savepath does not exist
        - savename or path was not given in correct format

    Returns
    -------
    Result : statsmodels.tsa.seasonal.DecomposeResult object
        Object containing the decomposition results

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
        plot_decomposition(Result,
                          title,
                          savepath = False,
                          savename = False,
                          ylabel = "Battery Level (%)",
                          xlabel  = "Date",
                          dates = False,
                          )
        
    return Result
    
def test_STL():
    res = STL_decomposition(setup_np(),'Test title', test=True) 
    assert res is not None
    assert res.observed.all() is not None
    assert res.trend.all() is not None
    assert res.seasonal.all() is not None
    assert res.resid.all() is not None
    
    test_argument = setup_pd()
    # Store information about raised ValueError in exc_info
    with pytest.raises(ValueError) as exc_info:
        STL_decomposition(test_argument,'Test title', test=True)
    expected_error_msg = "Series is not a numpy array."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
        
