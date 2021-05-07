#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:56:55 2020

@author: ikaheia1

Calculate the following summary statistics for the given timeseries and plot
the results:
    - Histogram
    - Lag plot with lag 1
    - Autocorrelation
    - Partial autocorrelation function
    - Autocorrelation function
    
"""
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from tscfat.Utils.plot_decorator import plot_decorator
from datetime import datetime
from matplotlib.dates import date2num

plt.style.use('seaborn')
plt.ioff()

#TODO! clean the code!
#TODO! fix the docstrings


@plot_decorator
def _plot_summary(series,
                  doi,
                  title,
                  window = 14,
                  savepath = False,
                  savename = False,
                  test = False
                  ):
    """ Plot summary statistic for the given timeseries.
    
    Parameters
    ----------
    series : Pandas Series
        A time series for which the surrary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    window : int
        Rolling window size. The default is 14.
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.

    Returns
    -------
    None.

    """
    fig,ax = plt.subplots(4,2,figsize=(12,12))
    fig.suptitle(title,fontsize=22,y=1)
    
    gridsize = (4,2)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=2,rowspan=1)
    ax2 = plt.subplot2grid(gridsize, (1,0), colspan=1,rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (1,1), colspan=1,rowspan=1)
    ax4 = plt.subplot2grid(gridsize, (2,0), colspan=1,rowspan=1)
    ax5 = plt.subplot2grid(gridsize, (2,1), colspan=1,rowspan=1)
    ax6 = plt.subplot2grid(gridsize, (3,0), colspan=1,rowspan=1)
    ax7 = plt.subplot2grid(gridsize, (3,1), colspan=1,rowspan=1)
    
    ax1.plot(series.index,series.values)
    ax1.set_title('Original timeseries',fontsize=18)
    ax1.tick_params('x', labelrotation=45)
    ax1.set_ylabel(ylabel='Value',fontsize=14)
    ax1.set_xlabel(xlabel='Date',fontsize=14)
    if doi is not None:
        #ax1.axvspan(int(date2num(datetime(*doi[0]))),int(date2num(datetime(*doi[1]))),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
        ax1.axvspan(15034,15126,ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    ax2.plot(series.index, series.rolling(window).mean())
    ax2.set_title('Rolling Average',fontsize=18)
    ax2.set_ylabel(ylabel='Rolling average',fontsize=14)
    ax2.set_xlabel(xlabel='Date',fontsize=14)
    
    ax3.hist(series.values,20)
    ax3.set_title("Histogram",fontsize=18)
    ax3.set_ylabel(ylabel='Value',fontsize=14)
    ax3.set_xlabel(xlabel='Count',fontsize=14)
  
    ax4.plot(series.values[1:],series.values[:-1],'o')
    ax4.set_title('Lag plot / lag 1',fontsize=18)
    ax4.set_ylabel(ylabel='t - 1',fontsize=14)
    ax4.set_xlabel(xlabel='t',fontsize=14)
    ax4.set_aspect(1)
      
    pd.plotting.autocorrelation_plot(series,ax=ax5)
    ax5.set_xlim([0,30])
    ax5.set_title('Autocorrelation',fontsize=18)
    ax5.set_ylabel(ylabel='Correlation',fontsize=14)
    ax5.set_xlabel(xlabel='Lag',fontsize=14)
    
    sm.graphics.tsa.plot_pacf(series,lags=30,ax=ax6)
    ax6.set_title('Partial autocorrelation function',fontsize=18)
    ax6.set_ylabel(ylabel='Correlation',fontsize=14)
    ax6.set_xlabel(xlabel='Lag',fontsize=14)
    
    sm.graphics.tsa.plot_acf(series,lags=30,ax=ax7)
    ax7.set_title('Autocorrelation function',fontsize=18)
    ax7.set_ylabel(ylabel='Correlation',fontsize=14)
    ax7.set_xlabel(xlabel='Lag',fontsize=14)
    
    fig.tight_layout(pad=1.0)
        
    return fig


def summary_statistics(series,
                       doi,
                       title = "Time series summary",
                       window = 14,
                       savepath = False,
                       savename = False,
                       test = False,
                       ):
    """ Calculate summary statistics for the give timeseries.
    
    Parameters
    ----------
    series : Pandas Series
        A time series for which the summary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    window : int
        Rolling window size. The default is 14.
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.
    test : Boolean, optional
        Flag for test function. The default is False.

    Returns
    -------
    None.

    """
    
    assert isinstance(series, pd.Series), "Series is not a pandas Series."
    
    _plot_summary(series,
                  doi,
                  title,
                  window,
                  savepath = savepath,
                  savename = savename,
                  test=False)

    
