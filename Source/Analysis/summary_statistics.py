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
from Source.Utils.argument_loader import setup_ps, setup_pd
import pytest
from Source.Utils.plot_decorator import plot_decorator
from matplotlib import gridspec

plt.style.use('seaborn')

@plot_decorator
def _plot_summary(series,
                  title,
                  savepath = False,
                  savename = False,
                  test = False
                  ):
    """
    
    Parameters
    ----------
    series : Pandas Series
        A time series for which the surrary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.

    Returns
    -------
    None.

    """

    
    fig,ax = plt.subplots(3,2,figsize=(10,10))
    fig.suptitle(title,fontsize=20,y=1)
    
    gridsize = (3,2)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=2,rowspan=1)
    ax2 = plt.subplot2grid(gridsize, (1,0), colspan=1,rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (1,1), colspan=1,rowspan=1)
    ax4 = plt.subplot2grid(gridsize, (2,0), colspan=1,rowspan=1)
    ax5 = plt.subplot2grid(gridsize, (2,1), colspan=1,rowspan=1)
    
    ax1.plot(series)
    ax1.set_title('Original timeseries')
    ax1.tick_params('x', labelrotation=45)
    
    series.rolling(14).mean().plot(ax=ax2)
    #sm.graphics.tsa.plot_pacf(series,lags=30,ax=ax5)
    ax2.set(title='Rolling Average',xlabel='date',ylabel='rolling average')
    
    ax3.hist(series,20)
    ax3.set_title("Histogram")
  
    pd.plotting.lag_plot(series,lag=1,ax=ax4)
    ax4.set_title('Lag plot / lag 1')
    ax4.set_box_aspect(1)
    #ax3.set(adjustable='box-forced', aspect='equal')
      
    pd.plotting.autocorrelation_plot(series,ax=ax5)
    ax5.set_xlim([0,30])
    ax5.set_title('Autocorrelation')
    
    #series.rolling(14).mean().plot(ax=ax5)
    #sm.graphics.tsa.plot_pacf(series,lags=30,ax=ax5)
    #ax5.set(xlabel='lag',ylabel='rolling average')
    
    #sm.graphics.tsa.plot_acf(series,lags=30,ax=ax[2,1])
    #ax[2,1].set(xlabel='lag',ylabel='correlation')
    
    fig.tight_layout(pad=1.0)
    
    #%%
    if all((savename,savepath)):
        
        assert isinstance(savename,str), "Invalid savename type."
    
        if savepath.exists():
            with open(savepath / (savename + "_summary.png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
    
    return fig


def summary_statistics(series,
                       title = "Time series summary",
                       savepath = False,
                       savename = False,
                       test = False):
    """
    

    Parameters
    ----------
    series : Pandas Series
        A time series for which the surrary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
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
    
    _plot_summary(series,title,savepath,savename,test=False)

    
def test_Summary_statistics():
    """
    Test Summary_statistics function. Test that Pandas data frame as an
    Sargument raises an error.

    Returns
    -------
    None.

    """
    
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        summary_statistics(setup_pd(),'Test title', savepath = False, savename = False, test = True)
    expected_error_msg = "Series is not a pandas Series."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)