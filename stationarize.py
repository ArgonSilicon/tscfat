#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:53:55 2020

@author: arsi
"""
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def test_stationarity(timeseries):
    
    assert isinstance(timeseries,np.ndarray), "Timeseries is of a type: {}, not np.ndarray".format(type(timeseries))
    
    result = adfuller(timeseries)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        nt('\t%s: %.3f' % (key, value))

def stationarize_timeseries(ts, method, argument):
    
    assert isinstance(ts,pd.core.series.Series),"Timeseries is not of a type pandas.core.series.Series."
    assert isinstance(method,str), "Method is not given as a string."
    
    try:
        if method == "transform":
            # argument is np.function
            stationarized_timeseries = argument(ts)
            
        elif method == "rolling_mean":
            # argument is window
            stationarized_timeseries = ts.rolling(window=argument).mean()    
        
        elif method == "difference":
            # argument is period
            stationarized_timeseries = ts.diff(periods=argument)
            
        """ include this ewm?
        series['ewm'] = series['Passengers'].ewm(com=0.5).mean()
        """
    
    except ValueError:
        print("Method was not of a valid type: transform, rolling_mean or difference.")
                    
    return stationarized_timeseries


if __name__ == "__main__":
    
    """ Can try something like this
    #1) first log, then diff
    series['diff'] = series['Passengers'].diff(periods=12)
    series['log_diff'] = series['log_t'].diff(periods=12)
    
    #2) first diff, then log
    X = series['diff'][12:]
    m = np.min(np.abs(X.iloc[X.values.nonzero()]))
    series['diff_log'] = np.log(X - (min(X) - m/2))
    """
    pass  