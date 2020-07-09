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

def process_screen_events(df):
    
    #%% filter
    df_filt = df.filter(["time","screen_status",])
    resampled = df_filt.resample("H").count()
    timeseries = resampled.values
    
    #%% calculate SSM and Novelty
    
    sim = calculate_similarity(timeseries,'euclidean')
    nov = compute_novelty_SSM(sim)
    Plot_similarity(sim,nov)
    
    #%% calculate receursion plot and metrics
    
    # Recursion plot settings
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.05 # neigborhood radius
    
    # Calculate recursion plot and metrix
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    
    #%% show recursion plot and save figure
    
    # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_4"
    TITLE = "Screen events / hourly Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
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
    
    return resampled
if __name__ == "__main__":
    pass