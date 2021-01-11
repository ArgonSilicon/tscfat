#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi

- Plot timeseries decomposition
- Plot similarity and novelty
- Plot rolling stats
- Plot clustering

"""

# standard library imports
from pathlib import Path

# third party imports
import numpy as np

# Local application import
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from decompose_timeseries import STL_decomposition#, detect_steps
from Plot_similarity import Plot_similarity
from timeseries_clustering import Cluster_timeseries
from Rolling_statistics import Rolling_statistics
from summary_statistics import Summary_statistics

def process_battery(df,FIGPATH):
    
    #%% filter dataframe and resample hourly means
    df_filt = df.filter(["time","battery_level",])
    df_grouped_lists = df_filt.battery_level.groupby(df_filt.index.hour).apply(list) # -> for grouped_histograms()
    resampled = df_filt.resample("H").mean()
    
    missing_values = resampled.isna()
    resampled_interpolated = resampled.interpolate('linear') 
    timeseries = resampled_interpolated.values
    
    
    # daily / hours for similarity calulation
    resampled_day = resampled_interpolated.resample('D').apply(list)
    data = np.stack(resampled_day.battery_level.values[1:-1])
    #%%
    _ = Summary_statistics(resampled_interpolated.battery_level,"Time series summary",False,False)
    
    #%% Plot timeseries decompostition and distribution for each component
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Decomposition')
    FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results/Decomposition')
    FIGNAME = "Battery_level_rolling_statistics" 
    _  = STL_decomposition(timeseries,"Battery level timeseries decomposition", False, FIGPATH,FIGNAME)
       
    #%% rolling stats
    w = 7*24
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\RollingStatistics')
    FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results/RollingStatistics')
    FIGNAME = "Battery_level_Rolling_Statistics"
    
    _ = Rolling_statistics(resampled_interpolated,w,FIGNAME,FIGPATH)
    
    
    #%% calculate similarity and novelty
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Similarity')
    FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results/Similarity')
    FIGNAME = "Battery_level_similarity"
    AXIS = resampled_day[1:-1].index.strftime('%m-%d')
    
    sim = calculate_similarity(data,'cosine')
    nov, kernel = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Battery level (cosine distance)",FIGPATH,FIGNAME,(0,0.04),0.9,AXIS,kernel)

    #%%
    # Timeseries clustering
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Clusters')
    FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results/Clusters')
    FIGNAME = "Clustered_timeseries"
    
    clusters = Cluster_timeseries(data,FIGNAME, FIGPATH, title="Battery level clustered timeseries",n=2)
     
   
    
    #%%
    return df, timeseries, data

if __name__ == "__main__":
    pass