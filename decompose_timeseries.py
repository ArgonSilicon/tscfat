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


    fig1 = plt.figure(figsize=(15,15))
    
    plt.suptitle('Timeseries decomposition',fontsize=20)
    
    plt.subplot(4,1,1)
    plt.plot(Result.observed)
    plt.title('Observations',fontsize=16)
    plt.ylabel("Battery Level")
    plt.xlabel("Time / hours")
                
    plt.subplot(4,1,2)
    plt.plot(Result.trend)
    plt.title('Trend',fontsize=16)
    plt.ylabel("Battery Level")
    plt.xlabel("Time / hours")
     
    plt.subplot(4,1,3)
    plt.plot(Result.seasonal)
    plt.title('Seasonal',fontsize=16)
    plt.ylabel("Battery Level")
    plt.xlabel("Time / hours")
     
    plt.subplot(4,1,4)
    plt.plot(Result.resid)
    plt.title('Residuals',fontsize=16)
    plt.ylabel("Battery Level")
    plt.xlabel("Time / hours")
    
    fig1.tight_layout(pad=4.0)
    
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
            
        
    fig2 = plt.figure(figsize=(20,15))
    
    plt.suptitle('Timeseries decomposition / histograms',fontsize=20)
    
    plt.subplot(2,2,1)
    plt.hist(Result.observed)
    plt.title('Observations',fontsize=16)
    plt.xlabel("Battery Level")
    plt.ylabel("Count")
                
    plt.subplot(2,2,2)
    plt.hist(Result.trend)
    plt.title('Trend',fontsize=16)
    plt.xlabel("Battery Level")
    plt.ylabel("Count")
    
    plt.subplot(2,2,3)
    plt.hist(Result.seasonal)
    plt.title('Seasonal',fontsize=16)
    plt.xlabel("Battery Level")
    plt.ylabel("Count")
     
    plt.subplot(2,2,4)
    plt.hist(Result.resid)
    plt.title('Residuals',fontsize=16)
    plt.xlabel("Battery Level")
    plt.ylabel("Count")
     
    fig2.tight_layout(pad=4.0)
    
    if not all((savename,savepath)):
        plt.show()
      
    elif all((savename,savepath)):
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + "_hist" + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
        
        
    return Result



def detect_steps(timeseries,
                 title,
                 xlabel,
                 savename = False,
                 savepath = False,
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
    savename : TYPE, optional
        DESCRIPTION. The default is False.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
     : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # signal
    sig = timeseries.values.reshape(-1,1)
    
    # window / kernel
    '''
    win = signal.gaussian(51,std=5).reshape(-1,1)
    win = np.gradient(win,axis=0)
    win = win - win.mean()
    win = win / win.max()
    '''
    # stepfunction
    win = -(np.array([0]*24+[1]*24).reshape(-1,1))
    
    
    # convolution
    filtered = signal.convolve(sig, win, mode='same') / sum(win)
    
    # find peaks / low points 
    peaks, properties = find_peaks(filtered.reshape(-1), height=0)
    bottoms, properties_b = find_peaks(-filtered.reshape(-1),height=0)
    heights = properties['peak_heights']
    lows = properties_b['peak_heights']
    
    # find top / low indices and values
    top_indices = heights.argsort()[-5:][::-1]
    top_peaks = peaks[top_indices]
    neg_indices = (lows).argsort()[-5:][::-1]
    neg_peaks = bottoms[neg_indices]

    # plot
    fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True,figsize=(15,10))
    plt.suptitle(title, fontsize=20)
    ax_orig.plot(sig)    
    ax_orig.set_ylabel('Original value')
    ax_orig.set_title('Original timeseries')
    ax_orig.margins(0, 0.1)
    ax_win.plot(win)
    ax_win.set_title('Kernel / filter')    
    ax_win.set_ylabel('Filter level')
    ax_win.margins(0, 0.1)
    ax_filt.plot(filtered)
    ax_filt.set_ylim(30,90)
    ax_filt.plot(neg_peaks, filtered[neg_peaks], "x", markersize=15, color="blue")    
    ax_filt.plot(top_peaks, filtered[top_peaks], "x", markersize=15, color="red")    
    ax_filt.set_title('Filtered timeseries')    
    ax_filt.set_ylabel('Filtered level')
    ax_filt.set_xlabel(xlabel)    
    ax_filt.margins(0, 0.1)
    fig.tight_layout()
    
    if not all((savename,savepath)):
        plt.show()
      
    elif all((savename,savepath)):
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + "_peaks" + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
    
    return peaks, bottoms, top_indices, neg_indices
    
    