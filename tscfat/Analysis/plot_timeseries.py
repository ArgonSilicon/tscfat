#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:44:59 2021

@author: arsi

Function for plotting dataframe columns containing the timeseries.

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tscfat.Utils.plot_decorator import plot_decorator

from datetime import datetime
from matplotlib.dates import date2num


sns.set_theme()

@plot_decorator
def plot_timeseries(data, columns, title, roll = False, xlab = "Date", ylab = "Value", ylim = False, savename = False, savepath = False, highlight = False, test=False):
    """ 
    Plot the selected columns of the given dataframe.  
    The dataframe index should be datetime object.
    
    
    Parameters
    ----------
    data : pandas dataframe
        Pandas dataframe containing the timeseries.
    columns : list
        A list of strings, containing the column names.
    title : str
        Figure name.
    roll : int, optional
        Rolling window length. The default is False.
    xlab : str, optional
        Figure x-label. The default is "Time".
    ylab : str, optional
        Figure y-label. The default is "Value".
    ylim : tuple, optional
        (float, float) ylimit for the figure. The default is False.
    savename : str, optional
        Figure savename. The default is False.
    savepath : path, optional
        Figure savepath. The default is False.
    highlight : tuple, optional
        Tuple containing the start and end point for the region highlighting. 
        The default is False.
    test : bool, optional
        Indicates whether the function is tested by pytest. 
        The default is False.

    Returns
    -------
    fig : matplotlib figure
        A figure containing the plotted timeseries.

    """        

    assert isinstance(data, pd.DataFrame), "Given data is not a pandas dataframe."
    assert isinstance(columns, list), "Given columns is not a list."
    
    fig , ax = plt.subplots(figsize=(15,10))
    
    if roll:
        data[columns].rolling(roll).mean().plot(color = ['g','r','k'], style = ['--','-.','-'], ylim=(0,1), ax=ax)
        
    else:
        data[columns].plot(color = ['g','r','k'], style = ['--','-.','-'], ylim=(0,1),ax=ax)
    
    if ylim:
        ax.set(ylim=(ylim))
        
    # TODO! fix the highlight not showing!

    if highlight:
        print('highlight')
        print(highlight[0],highlight[1])
        #ax.axvspan(highlight[0], highlight[1],facecolor="yellow", alpha=0.13, label="Days of interest")
        ax.axvspan(int(date2num(datetime(*highlight[0]))),int(date2num(datetime(*highlight[1]))),facecolor="yellow", alpha=0.13, label="Days of interest")
    #ax.axvspan(highlight[0], highlight[1], ymin=1, ymax=2, facecolor="yellow", alpha=0.13, label="Days of interest")
    ax.set_title(title, fontsize=26)
    ax.set_xlabel(xlab, fontsize=24)
    ax.set_ylabel(ylab, fontsize=24)
    ax.tick_params(axis='both', labelsize=20)
    ax.legend(loc = 'upper left',fontsize=18)
    
    plt.tight_layout(pad=1)
    
    return fig

