#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:44:59 2021

@author: arsi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from Source.Utils.plot_decorator import plot_decorator

@plot_decorator
def plot_timeseries(data, columns, title, roll = False, xlab = "Time", ylab = "Value", ylim = False, savename = False, savepath = False, highlight = False, test=False):
    """
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    columns : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    roll : TYPE, optional
        DESCRIPTION. The default is False.
    xlab : TYPE, optional
        DESCRIPTION. The default is "Time".
    ylab : TYPE, optional
        DESCRIPTION. The default is "Value".
    ylim : TYPE, optional
        DESCRIPTION. The default is False.
    savename : TYPE, optional
        DESCRIPTION. The default is False.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
    highlight : TYPE, optional
        DESCRIPTION. The default is False.
    test : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """        
    fig,ax = plt.subplots(figsize=(15,10))
    
    if roll:
        ax = data[columns].rolling(roll).mean().plot()
    else:
        ax = data[columns].plot(ax=ax)
    
    if ylim:
        ax.set(ylim=(ylim))
        
    # TODO! fix the highlight
    if highlight:
        ax.axvspan(highlight[0], highlight[1], ymin=0, ymax=1, facecolor="yellow", alpha=0.13, label="Days of interest")

    ax.set(title=title)
    ax.set(xlabel=xlab)
    ax.set(ylabel=ylab)
    
    return fig

