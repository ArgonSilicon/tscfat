#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:46:24 2021

@author: ikaheia1
"""
from datetime import datetime
from matplotlib.dates import date2num

def _doi2int(doi):
    """
    

    Parameters
    ----------
    doi : TYPE
        DESCRIPTION.

    Returns
    -------
    indices : TYPE
        DESCRIPTION.

    """
    
    indices = (date2num(datetime(*doi[0])),date2num(datetime(*doi[1])))
    return indices

def _ts2int(ts):
    """
    

    Parameters
    ----------
    ts : TYPE
        DESCRIPTION.

    Returns
    -------
    index : TYPE
        DESCRIPTION.

    """
    index = date2num(ts)
    return index

def doi2index(doi,df):
    """
    

    Parameters
    ----------
    doi : TYPE
        DESCRIPTION.
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    ind_s : TYPE
        DESCRIPTION.
    ind_e : TYPE
        DESCRIPTION.

    """
    
    #TODO! insert asserts here
    
    indices = _doi2int(doi)
    start = _ts2int(df.index[0])
    end =  _ts2int(df.index[-1])
    ind_s = indices[0] - start 
    ind_e = ind_s + (indices[1] - indices[0])
    
    return ind_s, ind_e