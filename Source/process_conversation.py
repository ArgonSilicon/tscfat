#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:54:37 2020

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

def process_conversation(df,key):
    
    df.rename(columns={' end_timestamp':'end_timestamp'}, inplace=True)
    df['start_timestamp'] = convert_to_datetime(df['start_timestamp'],units='s')
    df['end_timestamp'] = convert_to_datetime(df['end_timestamp'],units='s')
    df['duration'] = df.end_timestamp - df.start_timestamp 
    df['duration_s'] = df['duration'].dt.total_seconds()
    
   
    #%%
    timesum,tr = calculate_binned_conversation(df)
    timeseries = timesum.reshape(-1,1)
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL/Timeseries/')
    
    with open(FIGPATH / (key +".npy"), mode="wb") as outfile:
        np.save(outfile,timeseries)

    pd_series = pd.Series(timesum,index=tr)       
    
    #%% calculate SSM and Novelty
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL/Similarity/')
    FIGNAME = "similarity_" + key    
    sim = calculate_similarity(timeseries,'euclidean')
    nov = compute_novelty_SSM(sim,L=48)
    Plot_similarity(sim,nov,"Similarity and novelty",FIGPATH,FIGNAME)
    
    #%% calculate receursion plot and metrics
    
    # Recursion plot settings
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.15 # neigborhood radius
    
    # Calculate recursion plot and metrix
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    
    #%% show recursion plot and save figure
    
    # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL/Plots/')
    FIGNAME = "recplot_" + key
    TITLE = "Screen events / hourly Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    #%%
    # set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL/Metrics/')
    RESNAME = "metrics_" + key + ".json"
    dump_to_json(res,RESPATH,RESNAME)          
    
    #%%
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL/Timeseries/')
    TSNAME = "timeseries_" + key + ".mat"
    save2mat(timeseries,TSPATH,TSNAME)
    
    #%% Plot timeseries and save figure
    FIGNAME = "timeseries_scatter_" + key
    show_timeseries_scatter(pd_series,"Conversation / hourly binned seconds","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_line_" + key
    show_timeseries_line(pd_series,"Conversation / hourly binned seconds","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_features_" + key
    show_features(pd_series,"Conversation","xlab","ylab",48,1,'right',False,FIGPATH,FIGNAME)