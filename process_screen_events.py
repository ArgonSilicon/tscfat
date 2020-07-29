#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi
"""
# standard library imports
import os
from pathlib import Path
import json

# change correct working directory
WORK_DIR = Path('/u/26/ikaheia1/unix/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

# third party imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Local application import


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
from decompose_timeseries import STL_decomposition

def process_screen_events(df):
    
    #%% filter
    df_filt = df.filter(["time","screen_status",])
    df_filt_3 = df_filt[df_filt['screen_status'] == 3]
    
    resampled = df_filt.resample("H").count()
    resampled_3 = df_filt_3.resample("H").count()
    
    # for similarity
    resampled_day = resampled.resample('D').apply(list)
    data = np.stack(resampled_day.screen_status.values[1:-1])
    
    timeseries = resampled.values
    timeseries_3 = resampled_3.values
    
    #%% timeseries decompostition
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Decomposition/')
    FIGNAME = "decomposition_screen_events_3" 
    decomp = STL_decomposition(timeseries_3,FIGPATH,FIGNAME)
    
    
    #%% calculate SSM and Novelty
    print(data)
    sim = calculate_similarity(data,'cosine')
    nov = compute_novelty_SSM(sim)
    Plot_similarity(sim,nov,"Screen events",False,False,(0,0.05),0)
    
    #%% calculate SSM and Novelty 3
    
    sim_3 = calculate_similarity(timeseries_3,'euclidean')
    nov_3 = compute_novelty_SSM(sim_3)
    Plot_similarity(sim_3,nov_3)
    
    #%% calculate receursion plot and metrics
    
    # Recursion plot settings
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.05 # neigborhood radius
    
    # Calculate recursion plot and metrix
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    res_3, mat_3 = Calculate_RQA(timeseries_3,ED,TD,RA)
    
    #%% show recursion plot and save figure
    
    # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_4"
    TITLE = "Screen events / hourly Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
     # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_4_3"
    TITLE = "Screen events state 3/ hourly Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat_3,TITLE,FIGPATH,FIGNAME)
    
    # set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Metrics/')
    RESNAME = "metrics_4.json"
    dump_to_json(res,RESPATH,RESNAME)          
    
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Timeseries/')
    TSNAME = "timeseries_4.mat"
    save2mat(timeseries,TSPATH,TSNAME)
    #%% Plot timeseries and save figure
    FIGNAME = "timeseries_4"
    show_timeseries_scatter(df_filt.screen_status,"Screen events / hourly binned","time","Level",FIGPATH,FIGNAME)
    show_features(resampled['screen_status'],"Screen_events","xlab","ylab")
    
    FIGNAME = "timeseries_4_3"
    show_timeseries_scatter(df_filt_3.screen_status,"Screen events / hourly binned","time","Level",FIGPATH,FIGNAME)
    show_features(resampled_3['screen_status'],"Screen_events","xlab","ylab")
    
    return resampled, resampled_3
if __name__ == "__main__":
    pass