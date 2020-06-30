# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:04:26 2020

@author: arsii

This script consists of functions for converting unix time to Pandas datetime,
resampling the dataframe, calculating the rolling statistics, and plotting the 
timeseries.

"""

import os
import pandas as pd
from pathlib import Path
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


def convert_to_datetime(date, units = 'ms'):
    """
    Function converts given pandas series from unix time to datetime.

    Parameters
    ----------
    date : pandas series
        Dataframe column containing the time
    units : str (default = 'ms')
        Time unit conversion type
    
    Returns
    -------
    conv_date : pandas series
        Datetime converted pandas series
    
    """
    assert isinstance(date,pd.core.series.Series), "Timeseries should be Pandas series type."
    assert isinstance(units,str), "Unit type should be str, not {}".format(type(units))
    
    conv_date = pd.to_datetime(date,unit = units)
    return conv_date

def resample_dataframe(df, scale, column):
    """
    Function resamples pandas dataframe. Resampling loses all non-numeric
    columns, so it is advisable to use this function for plotting and 
    calculating statistics. Full documentation for Pandas resample function 
    can be found at:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html  

    Parameters
    ----------
    df : pandas dataframe
        Dataframe to be resampled
    scale : str 
        Time offset alias. A comlete list of abbreviations can be found at: 
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    colum : pandas series
        The column by which the dataframe is resampled
    Returns
    -------
    df_rs : pandas dataframe
        Resampled dataframe
    
    """
    df_rs = df.resample(scale, on=column).mean().reset_index().sort_values(by=column)
    return df_rs

def rolling_statistics(series,roll,func):
    """
    Function calculates rolling windows statistic for given pandas series. 

    Parameters
    ----------
    series : pandas series
        Time series on which the rolling statistics is calculated.
    roll: int 
        Rolling window side.
    function : ???
        Function for statistics, implement this!
    Returns
    -------
    rs : pandas series
        Rolling statistics time series.
    
    """
    rs = series.rolling(roll).apply(lambda x: x.var(), raw=False)
    return rs

def plot_roll_stats(rs,title,xlab,ylab,savename = False, savepath = False):
    """
    Function plots given rolling statistics. Optionally, the plot can be saved 
    on a disk.

    Parameters
    ----------
    rs : pandas series
        Timeseries to be plotted.
    title : str
        Plot title
    xlab : str
        Plot xlabel
    ylab : str
        Plot ylabel
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where plot is to be saved. Path has to exist before calling this 
        function.

    Returns
    -------

    """
    assert isinstance(rs, pd.core.series.Series), "Timeseries should be Pandas series type."
    assert all(isinstance(i, str) for i in [title, xlab, ylab]), "Plot arguments should be strings."
        
    plt.plot(rs)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
    if not savename and not savepath:
        plt.show()
        
    elif savename and savepath:
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")

if __name__ == "__main__":
    # this code is for testing purposes only
    data_folder = Path(r'/home/arsi/Documents/SpecialAssignment/StudentLife/dataset/call_log/')
    files = os.listdir(data_folder)
    csv_list = []
    #%%
    for name in files:
        read_name = data_folder / name
        csv_list.append(pd.read_csv(read_name))

    df = csv_list[0]
    #%%
    UNITS = 'ms'
    df['CALLS_date'] = convert_to_datetime(df['CALLS_date'],UNITS)
    df_resampled = resample_dataframe(df, 'D', 'CALLS_date')
    #%%
    rolls = rolling_statistics(df_resampled['CALLS_duration'],7, 'autocorr')
    title = 'Calls duration / rolling window autocorrelation'
    xlab = 'TIme / days'
    ylab = 'Autocorrelation'
    plot_roll_stats(rolls,title,xlab,ylab)