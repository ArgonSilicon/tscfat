
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:31:11 2020

@author: ikaheia1
"""
import os
import pandas as pd
from pathlib import Path

def setup_np():
    
    open_name = Path.cwd() / 'Data' / 'Test_data.csv'
    
    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        return df['level'].values
    

def setup_ps():

    open_name = Path.cwd() / 'Data' / 'Test_data.csv'

    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        return df['level']
  
def setup_pd():
    
    open_name = Path.cwd() / 'Data' / 'Test_data.csv'

    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file, index_col=0)
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        return df
