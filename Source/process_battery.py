#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi
"""

# standard library imports
import os
from pathlib import Path
#import json

# third party imports
import numpy as np
#import matplotlib.pyplot as plt
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


def process_battery(df,FIGPATH):
    
    #%% Recursion plot settings
    '''
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.5 # neigborhood radius
    '''
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
       
    #%% plot differences and detect steps
    '''
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Differences/')
    FIGNAME = "Battery_level"
    lowest, diff, pct = plot_differences(resampled_interpolated, "battery_level","Battery level change in time", "Time (h)", "Difference",FIGPATH,FIGNAME)
    #%%
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Decomposition/')
    FIGNAME = "Steps"
    peaks, bottoms, top_indices, neg_indices = detect_steps(resampled_interpolated, "Battery level peaks and bottoms", "Time (h)",FIGPATH,FIGNAME)
    #%%
    high_ts = resampled_interpolated.index[peaks[top_indices]]    
    low_ts = resampled_interpolated.index[bottoms[neg_indices]]
    print("Differencing: ")
    print("Highest battery comsumption:\n",lowest.index)
    print("Gaussian kernel convolution: ")
    print("Highest peaks in battery charge:\n", high_ts)
    print("Highest battery consumption:\n",low_ts)
    #%% timeseries decompostition
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Decomposition/')
    FIGNAME = "Battery_level_decomposition" 
    decomp = STL_decomposition(timeseries,"Battery level timeseries decomposition", FIGPATH,FIGNAME)
        
    #%% calculate receursion plot and metrics
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
        
    #%% show recursion plot and save figure
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "Battery_level_RP"
    TITLE = "Battery level Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)   
    '''
    #%% calculate similarity and novelty
    FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Similarity')
    FIGNAME = "Battery_level_similarity"
    AXIS = resampled_day[1:-1].index.strftime('%m-%d')
    
    sim = calculate_similarity(data,'cosine')
    nov, kernel = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Battery level (cosine distance)",FIGPATH,FIGNAME,(0,0.04),0.9,AXIS,kernel)
    '''
    #Plot_similarity(sim,nov,"Battery level (cosine distance)",FIGPATH,FIGNAME,
    #                ylim = (0,0.05),threshold = 0,axis = AXIS, kernel)
    
    #%% set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Metrics/')
    RESNAME = "Battery_level_RP_metrics.json"
    dump_to_json(res,RESPATH,RESNAME)   
    
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Timeseries/')
    TSNAME = "Battery_level_ts.mat"
    save2mat(timeseries,TSPATH,TSNAME)
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Timeseries/')
    NPNAME = "Battery_level_ts.npy"
    with open(FIGPATH / NPNAME, mode="wb") as outfile:
        np.save(outfile,timeseries)       
    
    #%% Plot timeseries and save figure
    FIGNAME = "Battery_level_ts_scatter"
    show_timeseries_scatter(resampled_interpolated['battery_level'],"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "Battery_level_ts_line"
    show_timeseries_line(resampled_interpolated['battery_level'],"Battery level / hourly mean","time","Level",FIGPATH,FIGNAME)
    #%% Extract features from timeseries, plot, and save
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Features/')
    FIGNAME = "Battery_level_features"
    show_features(resampled_interpolated['battery_level'],"Battery level ","Time (d)","Value",24,1,"right",False,FIGPATH,FIGNAME)
    '''

    #%%
    return df, timeseries, data

if __name__ == "__main__":
    pass