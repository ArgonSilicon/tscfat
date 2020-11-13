#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 10:54:02 2020

@author: ikaheia1
"""
# standard library imports
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# change correct working directory
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

# Local application imports
from csv_load import load_all_subjects
from rolling_stats import convert_to_datetime
from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler, normalize_values
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
from save_results import dump_to_json
from plot_timeseries import show_timeseries_scatter, show_features
from save2mat import save2mat
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from json_load import load_one_subject
from Plot_similarity import Plot_similarity
from interpolate_missing import interpolate_missing
from plot_timeseries import show_timeseries_scatter, show_timeseries_line, show_features
from binned_conversation import calculate_binned_conversation
from decompose_timeseries import STL_decomposition


def process_call_logs(df,key):
    
    if "CALLS_duration" not in df.columns:
        return None
    
    df['start_timestamp'] = df.index
    df['CALLS_duration'] = pd.to_timedelta(df['CALLS_duration'], unit='s')
    df['end_timestamp'] = df['start_timestamp'] + df['CALLS_duration']

    #filter out nan's
    df_filt = df[df['CALLS_duration'].notnull()]
    df_filt = df_filt.filter(items=['start_timestamp', 'end_timestamp'])
   
    #%%
    timesum,tr = calculate_binned_conversation(df_filt)
    timeseries = timesum.reshape(-1,1)
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Timeseries/')
    
    with open(FIGPATH / (key +".npy"), mode="wb") as outfile:
        np.save(outfile,timeseries)

    pd_series = pd.Series(timesum,index=tr)       
    
    #%% some resampling
    #resampled = pd_series.resample("D").apply(custom_resampler)
    resampled = pd_series.resample("D").apply(np.sum)
    #timeseries = resampled.values
    #timeseries = np.stack(timeseries)
    #timeseries = np.stack(timeseries[1:-1])
    
    #%% decompostition
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Decomposition/')
    FIGNAME = "decomposition_" + key
    decomp = STL_decomposition(resampled,FIGPATH,FIGNAME)
    
    # get trend from decomposition
    trend = decomp.trend.values.reshape(-1,1)
    
    #%% calculate SSM and Novelty
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Similarity/')
    FIGNAME = "similarity_" + key    
    sim = calculate_similarity(trend,'euclidean')
    nov = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Call events trend / Similarity and novelty",FIGPATH,FIGNAME)
    
    #%% calculate receursion plot and metrics
    
    # Recursion plot settings
    ED = 1# embedding dimensions
    TD = 1# time delay
    RA = 1 # neigborhood radius
    
    # Calculate recursion plot and metrix
    res, mat = Calculate_RQA(trend,ED,TD,RA)
    #res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    
    #%% show recursion plot and save figure
    
    # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Plots/')
    FIGNAME = "recplot_" + key
    TITLE = "Call events trend / daily Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    #%%
    # set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Metrics/')
    RESNAME = "metrics_" + key + ".json"
    dump_to_json(res,RESPATH,RESNAME)          
    
    #%%
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Timeseries/')
    TSNAME = "timeseries_" + key + ".mat"
    save2mat(timeseries,TSPATH,TSNAME)
    
    #%% Plot timeseries and save figure
    FIGNAME = "timeseries_scatter_" + key
    show_timeseries_scatter(pd_series,"Call events / daily binned totals","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_line_" + key
    show_timeseries_line(pd_series,"Call events / daily binned totals","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_features_" + key
    show_features(pd_series,"Call events / daily binned totals","xlab","ylab",48,1,'right',False,FIGPATH,FIGNAME)
    
