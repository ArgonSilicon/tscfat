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
import os
from pathlib import Path
#import json

# third party imports
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
#from scipy import signal

# Local application import



#from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler, normalize_values
#from calculate_RQA import Calculate_RQA
#from plot_recurrence import Show_recurrence_plot
#from save_results import dump_to_json
from plot_timeseries import show_timeseries_scatter, show_timeseries_line, show_features, plot_differences, grouped_histograms
#from save2mat import save2mat
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from decompose_timeseries import STL_decomposition#, detect_steps
from Plot_similarity import Plot_similarity
from interpolate_missing import interpolate_missing
#from calculate_DTW import DTW_distance
from timeseries_clustering import Cluster_timeseries
from arma import arma, autocorr

def process_battery(df,FIGPATH):
    
    #%% filter dataframe and resample hourly means
    df_filt = df.filter(["time","battery_level",])
    df_grouped_lists = df_filt.battery_level.groupby(df_filt.index.hour).apply(list) # -> for grouped_histograms()
    resampled = df_filt.resample("H").mean()
    resampled_interpolated, _ = interpolate_missing(resampled,'linear')
    timeseries = resampled_interpolated.values
    
    # daily / hours for similarity calulation
    resampled_day = resampled_interpolated.resample('D').apply(list)
    data = np.stack(resampled_day.battery_level.values[1:-1])
    
    #%% plot histograms
    FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Distributions')
    FIGNAME = "Battery_level" 
    grouped_histograms(df_grouped_lists,'Battery level','Percentage','Proportion',FIGPATH,FIGNAME)
    
    #%% Plot timeseries decompostition and distribution for each component
    FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Decomposition')
    FIGNAME = "Battery_level_decomposition" 
    _  = STL_decomposition(timeseries,"Battery level timeseries decomposition", False, FIGPATH,FIGNAME)
       
    #%% rolling stats
    w = 7*24
    variance = resampled_interpolated.rolling(window = w).var()
    autocorrelation = resampled_interpolated.rolling(window = w).apply(autocorr)
    mean = resampled_interpolated.rolling(window = w).mean() 
    skew = resampled_interpolated.rolling(window = w).skew()
    kurt = resampled_interpolated.rolling(window = w).kurt()
    
    plt.plot(variance)
    plt.title('variance')
    plt.show()
    
    plt.plot(autocorrelation)
    plt.title('autocorrelation')
    plt.show()
    
    plt.plot(mean)
    plt.title('mean')
    plt.show()
    
    plt.plot(skew)
    plt.title('skew')
    plt.show()
    
    plt.plot(kurt)
    plt.title('kurt')
    plt.show()
    
    #%% calculate similarity and novelty
    FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Similarity')
    FIGNAME = "Battery_level_similarity"
    AXIS = resampled_day[1:-1].index.strftime('%m-%d')
    
    sim = calculate_similarity(data,'cosine')
    nov, kernel = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Battery level (cosine distance)",FIGPATH,FIGNAME,(0,0.04),0.9,AXIS,kernel)

    #%%
    # Timeseries clustering
    clusters = Cluster_timeseries(data,n=2)
    plt.plot(clusters,'o')
    plt.show()
    
    #%%
    return df, timeseries, data

if __name__ == "__main__":
    pass