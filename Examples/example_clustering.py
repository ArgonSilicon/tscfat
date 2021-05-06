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
import numpy as np

from config_clustering import fn, ap, doi
os.chdir('/home/arsii/tscfat')

from tscfat.Analysis.cluster_timeseries import cluster_timeseries
from tscfat.Utils.doi2int import doi2index


#%% LOAD THE DATA FRAME AND PREPARE THE DATA FOR CLUSTERING
df = pd.read_csv(fn.csv_path, index_col = 0)
df.index = pd.to_datetime(df.index)
df = df.resample('H').mean()
df = df.interpolate()
df = df.resample('D').apply(list)
df = df['2015-03-26':'2015-12-03']
data = np.stack(df.battery_level.values)

#%%
ind_s, ind_e = doi2index(doi,df)

#%% SUMMARY STATISTICS 
print('Processing Timeseries Clustering: \n')

clusters = cluster_timeseries(data,
                              FIGNAME = fn.clustering_base,
                              FIGPATH = fn.clustering_out,
                              title = '{} clusters'.format(df.columns[0]), 
                              n = ap.n, 
                              mi = ap.mi, 
                              mib = ap.mib, 
                              rs = ap.rs, 
                              metric = ap.metric, 
                              highlight = (ind_s,ind_e),
                              ylim_ = ap.ylim)
    
print('Done.')
    

