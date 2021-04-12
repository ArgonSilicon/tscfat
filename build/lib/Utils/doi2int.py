#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:46:24 2021

@author: ikaheia1

A helper function for converting the datetime to indices used for plotting.
"""
import pandas as pd
from datetime import datetime
from matplotlib.dates import date2num

def _doi2int(doi):
    """
    Convert tuple of two datetime objects to Matplotlib dates. 
    

    Parameters
    ----------
    doi : tuple
        Tuple contains two datetime objects.

    Returns
    -------
    indices : float
        Number of days since the unix time epoch.

    """
    assert isinstance(doi, tuple), "Doi is not a tuple."
    
    indices = (date2num(datetime(*doi[0])),date2num(datetime(*doi[1])))
    return indices

def _ts2int(ts):
    """
    Convert a datetime objects to Matplotlib date.

    Parameters
    ----------
    ts : datetime.datetime or numpy.datetime64
        A datetime object.

    Returns
    -------
    index : float
        Number of days since the unix time epoch.

    """
    assert isinstance(ts, pd._libs.tslibs.timestamps.Timestamp), "Timestamp is not in datetime format"
   
    index = date2num(ts)
    return index

def doi2index(doi,df):
    """ 
    Convert given range given in datetime objects into corresponding 
    Matplotlib indices, that are used to highligh the region in analysis 
    figures. 
    

    Parameters
    ----------
    doi : tuple
        Contain two datetime objects.
    df : pandas DataFrame
        A dataframe with datetime index.

    Returns
    -------
    ind_s : float
        Starting index. Number of days since the unix time epoch.
    ind_e : float
        End index. Number of days since the unix time epoch.

    """
    
    assert isinstance(doi, tuple), "Doi is not a tuple."
    assert isinstance(doi[0], tuple), "The first item in tuple is not a tuple."
    assert isinstance(doi[1], tuple), "The second item in tuple is not a tuple."
    assert isinstance(df, pd.DataFrame), "df is not a pandas dataframe."
    
    indices = _doi2int(doi)
    start = _ts2int(df.index[0])
    end =  _ts2int(df.index[-1])
    ind_s = indices[0] - start 
    ind_e = ind_s + (indices[1] - indices[0])
    
    return ind_s, ind_e