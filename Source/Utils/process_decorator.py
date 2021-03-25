#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:23:43 2021

@author: arsi

Function wrapper for iterating dataframe columns.
"""
import functools
import pandas as pd

def process_decorator(func):
    @functools.wraps(func)
    def wrapper(df,cols):
        assert isinstance (df, pd.DataFrame), "Given argument df is not a pandas dataframe."
        assert isinstance (cols, list), "Given argument cols is not a list."
        
        for i, name in enumerate(cols):
           
            if type(name) == list:
                names = " - ".join(name)
                print('Column: {:30s} : {}/{}'.format(names, i+1, len(cols)))
                
            else:
                print('Column: {:30s} : {}/{}'.format(name, i+1, len(cols)))
            
            func(df,name)
    return wrapper