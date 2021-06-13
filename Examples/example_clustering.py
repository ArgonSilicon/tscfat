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
#df = pd.read_csv(fn.csv_path, index_col = 0)
#TODO! please, remove this!
df = pd.read_csv('/home/arsii/Data/Battery.csv', index_col = 0, header=0)
df.time = pd.to_datetime(df.time, unit='s', origin = 'unix')
df = df.set_index(df.time)
df = df.filter(['battery_level'])

df = df.resample('H').mean()
df = df.interpolate()
df = df.resample('D').apply(list)
df = df['2020-06-26':'2021-02-09']
data = np.stack(df.battery_level.values)
df.index = pd.date_range(start='29/06/2011', end='02/12/2012')

#%%
doi = ((2011, 10, 1), (2011, 12, 24))
ind_s, ind_e = doi2index(doi,df)

#%% SUMMARY STATISTICS 
print('Processing Timeseries Clustering: \n')

clusters = cluster_timeseries(data,
                              FIGNAME = False,
                              FIGPATH = False,
                              title = 'Daily clusters: battery level', 
                              n = ap.n, 
                              mi = ap.mi, 
                              mib = ap.mib, 
                              rs = ap.rs, 
                              metric = ap.metric, 
                              highlight = (ind_s,ind_e),
                              ylim_ = ap.ylim)
    
print('Done.')

'''
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
'''  
#%% PLEASE REMOVE THESE!!
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
fig = plt.figure(figsize=(10,10))
#TODO! please remove this
dayz = pd.date_range(start='29/06/2011', end='02/12/2012')

plt.plot(clusters +1, dayz ,'o:')
'''
plt.axvspan(int(date2num(datetime(*doi[0]))),
           int(date2num(datetime(*doi[1]))),
           facecolor="yellow",
           alpha=0.13, 
           label="Days of interest")
'''
plt.title('title',fontsize=26)
plt.xlabel('xlab', fontsize=24)
plt.ylabel('ylab', fontsize=24)
plt.yticks(np.arange(1,6))
plt.tick_params(axis='both', labelsize=20)
plt.plot(dayz,df.cluster,'b:o')
plt.show()