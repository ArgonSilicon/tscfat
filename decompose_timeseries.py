#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:40:46 2020

@author: arsi
"""
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose,STL


def STL_decomposition(series,
                      savepath = False,
                      savename = False):
    """
    STL Decompose timeseries into Model, Trend, Seasonal and Residual parts.

    Parameters
    ----------
    series : TYPE
        DESCRIPTION.
    
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


    fig = plt.figure(figsize=(15,15))
    
    plt.suptitle('Timeseries decomposition',fontsize=20)
    
    plt.subplot(4,1,1)
    plt.plot(Result.observed)
    plt.title('Observations',fontsize=16)
                
    plt.subplot(4,1,2)
    plt.plot(Result.trend)
    plt.title('Trend',fontsize=16)
     
    plt.subplot(4,1,3)
    plt.plot(Result.seasonal)
    plt.title('Seasonal',fontsize=16)
     
    plt.subplot(4,1,4)
    plt.plot(Result.resid)
    plt.title('Residuals',fontsize=16)
    
    fig.tight_layout(pad=4.0)
    
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
            
    return Result
    