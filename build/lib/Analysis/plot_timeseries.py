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


sns.set_theme()

@plot_decorator
def plot_timeseries(data, columns, title, roll = False, xlab = "Time", ylab = "Value", ylim = False, savename = False, savepath = False, highlight = False, test=False):
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
    assert isinstance(columns, list), "Given columsn is not a list."
    
    
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

