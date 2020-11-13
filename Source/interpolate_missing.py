#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:05:03 2020

@author: arsi
"""

import pandas as pd
import numpy as np

def interpolate_missing(ts, interpolation):
    
    """
    Impute time series missing values using pandas interpolate function 
    with given method.
    
    Parameters
    ----------
    ts : Pandas series
        Pandas series to be inrpolated 
    interpolation : str
        Intepolatio method 

    Returns
    -------
    interpolated_ts : pandas series
        Imputed time series
    missing_values : pandas series
        Missing values indicated by booleans 

    """
    
    missing_values = ts.isna()
    
    interpolated_ts = ts.interpolate(interpolation)    
    
    return interpolated_ts, missing_values

if __name__ == "__main__":
    pass