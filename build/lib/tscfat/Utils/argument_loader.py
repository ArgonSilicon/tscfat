
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:31:11 2020

@author: ikaheia1

Helper functions for pytest test data loading.
Load a csv file and convert it using separate loading functions for:
    1) Numpy array format
    2) Pandas series format
    3) Pandas dataframe format

"""

import pandas as pd
from pathlib import Path

# TODO convert theses into single function!
'''
def setup_data(open_name, ret_type):
     
    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        
        if ret_type == 'numpy':
            return df['level'].values
        elif ret_type == 'series':
            return df['level']
        else:
            return df
'''
    
def setup_np():
    """
    Load the test data and convert the values into 1D numpy array.

    Returns
    -------
    _ = numpy array
        A 1D numpy array containing the test data time series.

    """
    
    open_name = Path.cwd() / 'Data' / 'Test_data.csv'
    
    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df.index = pd.to_datetime(df.index)
        #df['time'] = pd.to_datetime(df['time'])
        #df = df.set_index('time')
        return df['level'].values
    

def setup_ps():
    """
    Load the test data and convert the values into pandas Series.

    Returns
    -------
    _ = pandas Series
        A pandas series containing the test data time series.

    """

    open_name = Path.cwd() / 'Data' / 'Test_data.csv'

    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df.index = pd.to_datetime(df.index)
        #df['time'] = pd.to_datetime(df['time'])
        #df = df.set_index('time')
        return df['level']
  
def setup_pd():
    """
    Load the test data and convert the values into pandas DataFrame.

    Returns
    -------
    _ = pandas DataFrame
        A pandas DataFrame containing the test data time series.

    """
    
    open_name = Path.cwd() / 'Data' / 'Test_data.csv'

    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df.index = pd.to_datetime(df.index)
        #df['time'] = pd.to_datetime(df['time'])
        #df = df.set_index('time')
        return df
