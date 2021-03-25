#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:23:43 2021

@author: arsi

Function wrapper for iterating dataframe columns.
"""
import functools

def process_decorator(func):
    @functools.wraps(func)
    def wrapper(df,cols):
        for i, name in enumerate(cols):
           
            if type(name) == list:
                names = " - ".join(name)
                print('Column: {:30s} : {}/{}'.format(names, i+1, len(cols)))
                
            else:
                print('Column: {:30s} : {}/{}'.format(name, i+1, len(cols)))
            
            func(df,name)
    return wrapper