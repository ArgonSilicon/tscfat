#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is the example script for battery level processing. 
The data is loaded in CSV format. 
The analysis is conducted in process_battery_level.py.
The results are stored on disk.

"""
import os
import pandas as pd

os.chdir('/u/26/ikaheia1/data/Documents/tscfat')  # Provide the new path here

from config import fn, ap, doi

from Source.Analysis.summary_statistics import summary_statistics
from Source.Analysis.rolling_statistics import rolling_statistics


#%%
print(fn.csv_path)
print(fn.list_filenames())

#%% LOAD THE DATA FRAME
df = pd.read_csv(fn.csv_path)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])
df = df.drop(columns=['date','Other','Work/Study'])

#%% SUMMARY STATISTICS
print('Processing Summary Statistics: ')

for i, name in enumerate(df.columns.to_list()):        
    print('Column: {:30s} : {}/{}'.format(name,i,df.shape[1]))
    ser = df[name] 
    _ = summary_statistics(ser,
                           "{} summary".format(name),
                           ap.summary_window,
                           fn.summary_out,
                           fn.summary_base + '_' + name,
                           False)
    

#%% ROLLING STATISTICS 
print("Processing Rolling Statistics: ")
i = 1
for name in df.columns.to_list():
    print('Column: {:30s} : {}/{}'.format(name,i,df.shape[1]))
    i += 1
    ser = df[name] 
    savename = fn.rolling_base + '_' + name
    _ = rolling_statistics(ser.to_frame(),
                           ap.rolling_window,
                           doi = doi,
                           savename = savename,
                           savepath = fn.rolling_out,
                           test = False)
    
#%% TIMESERIES DECOMPOSITION


