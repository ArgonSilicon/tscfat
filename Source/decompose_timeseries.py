#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:40:46 2020

@author: arsi

Calculate STL decomposition for given time series and plot the components.

"""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from setup import setup_np, setup_pd
import pytest
from plot_decorator import plot_decorator

@plot_decorator
def __plot_decomposition(Result,
                      title,
                      savepath = False,
                      savename = False,
                      ylabel = "Battery Level (%)",
                      xlabel  = "Date",
                      dates = False,
                      ):
    """
    Plot the decomposed time series.

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
        

    Raises
    ------
    Exception
        - savepath does not exist
        - savename or path was not given in correct format

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
        - given series is not a numpy array.
        

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
        __plot_decomposition(Result,
                          title,
                          savepath = savepath,
                          savename = savename,
                          ylabel = "Battery Level (%)",
                          xlabel  = "Date",
                          dates = False,
                          )
        
    return Result
    
def test_STL():
    """
    Test STL_decomposition function. Test passes with proper arguments and 
    raises an AssertionError if the input time series is not numpy array.

    Returns
    -------
    None.

    """
    res = STL_decomposition(setup_np(),'Test title', test=True) 
    assert res is not None
    assert res.observed.all() is not None
    assert res.trend.all() is not None
    assert res.seasonal.all() is not None
    assert res.resid.all() is not None
    
    test_argument = setup_pd()
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        STL_decomposition(test_argument,'Test title', test=True)
    expected_error_msg = "Series is not a numpy array."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
        
