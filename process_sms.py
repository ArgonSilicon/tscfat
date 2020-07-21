#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 15:17:17 2020

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

def process_sms(df,key):
    
    df["count"] = 1
    df_filt = df.filter(items=['count',])
    resampled = df_filt.resample("H").apply(np.sum)
    timeseries = resampled['count'].values.reshape(-1,1)
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_3/Timeseries/')
    
    with open(FIGPATH / (key +".npy"), mode="wb") as outfile:
        np.save(outfile,timeseries)
       
    #%% decomposition
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_3/Decomposition/')
    FIGNAME = "decomposition_" + key
    decomp = STL_decomposition(timeseries,FIGPATH,FIGNAME)
    # get trend from decomposition
    trend = decomp.trend.reshape(-1,1)
    
    
    #%% calculate SSM and Novelty
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_3/Similarity/')
    FIGNAME = "similarity_" + key    
    sim = calculate_similarity(trend,'euclidean')
    nov = compute_novelty_SSM(sim,L=24)
    Plot_similarity(sim,nov,"Similarity and novelty",FIGPATH,FIGNAME)
    
    #%% calculate receursion plot and metrics
    
    # Recursion plot settings
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.15 # neigborhood radius
    
    # Calculate recursion plot and metrix
    res, mat = Calculate_RQA(trend,ED,TD,RA)
    
    #%% show recursion plot and save figure
    
    # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_3/Plots/')
    FIGNAME = "recplot_" + key
    TITLE = "SMS / hourly Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    #%%
    # set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_3/Metrics/')
    RESNAME = "metrics_" + key + ".json"
    dump_to_json(res,RESPATH,RESNAME)          
    
    #%%
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_3/Timeseries/')
    TSNAME = "timeseries_" + key + ".mat"
    save2mat(timeseries,TSPATH,TSNAME)
    
    #%% Plot timeseries and save figure
    FIGNAME = "timeseries_scatter_" + key
    show_timeseries_scatter(resampled,"SMS / hourly binned count","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_line_" + key
    show_timeseries_line(resampled,"SMS / hourly binned count","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_features_" + key
    show_features(resampled,"SMS","xlab","ylab",24,1,'right',False,FIGPATH,FIGNAME)
    