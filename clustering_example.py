#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:01:11 2021

@author: arsii
"""

import pandas as pd
import numpy as np

from tscfat.Analysis.cluster_timeseries import cluster_timeseries

#%% LOAD THE DATA FRAME
df = pd.read_csv('/home/arsi/Documents/tscfat/Data/Battery_test_data.csv',index_col=0)

df.index = pd.to_datetime(df.index)

df = df.resample('H').mean()

df = df.interpolate()

df = df.resample('D').apply(list)

df = df[1:-1]

data = np.stack(df.battery_level.values)

clusters = cluster_timeseries(data,
                              FIGNAME = False,
                              FIGPATH = False,
                              title = 'Battery Level Clustering Example', 
                              n = 5, 
                              mi = 5, 
                              mib = 5, 
                              rs = 0, 
                              metric = 'dtw', 
                              highlight = None,
                              ylim_ = None)