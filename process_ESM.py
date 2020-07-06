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
WORK_DIR = Path(r'/home/arsi/Documents/SpecialAssignment/CS-special-assignment/')
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
from plot_timeseries import show_timeseries, show_features
from save2mat import save2mat
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from json_load import load_one_subject
from Plot_similarity import Plot_similarity
from interpolate_missing import interpolate_missing


def process_ESM(df):
    
    #%% Recursion plot settings
    ED = 2 # embedding dimensions
    TD = 2 # time delay
    RA = 0.15 # neigborhood radius
    
    #%%
    mask1 = df["type"] == 1
    mask2 = df["type"] == 2
    mask3 = df["type"] == 3
    mask6 = df["type"] == 6
    df['Scaled_answer'] = 0
    
    df.loc[mask1,"answer"] = df.loc[mask1,"answer"].map(decode_string)
    df.loc[mask2,"answer"] = df.loc[mask2,"answer"].map(decode_string)
    df.loc[mask3,"answer"] = df.loc[mask3,"answer"].map(decode_string_3)
    
    df.loc[mask1,"Scaled_answer"] = df.loc[mask1,"answer"] 
    df.loc[mask2,"Scaled_answer"] = df.loc[mask2,"answer"] 
    df.loc[mask3,"Scaled_answer"] = normalize_values(df.loc[mask3,"answer"].values.astype(float))
    df.loc[mask6,"Scaled_answer"] = normalize_values(df.loc[mask6,"answer"].values.astype(float))
    
    #%%
    #df_filt = df.filter(["time","Scaled_answer",])
    df_filt = df.filter(["time","answer",])
    #df_filt = df_filt["Scaled_answer"].astype(int)
    df_filt = df_filt["answer"].astype(int)
    resampled = df_filt.resample("D").apply(custom_resampler)
    
    #%%
    timeseries = resampled.values
    timeseries = np.stack(timeseries[:-1])
    print(timeseries.shape)
    #%% calculate receursion plot and metrics
    # similarity
    sim = calculate_similarity(timeseries,'euclidean')
    nov = compute_novelty_SSM(sim,L=2)
    sim[sim >= 0.11] = 1
    Plot_similarity(sim,nov)
    #%% Calculate recursion plot and metrix
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    
    #%% show recursion plot and save figure
    
    # set correct names and plot title
    FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_2"
    TITLE = "ESM Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    # set correct names and save metrics as json 
    RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
    RESNAME = "metrics_2.json"
    dump_to_json(res,RESPATH,RESNAME)  
    
    # save the timeseries
    TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
    TSNAME = "timeseries_2.mat"
    save2mat(timeseries,TSPATH,TSNAME)        
    
    #%% Plot timeseries and save figure -> How to plot these!!!
    #FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
    #FIGNAME = "timeseries_2"
    #show_timeseries(resampled.index,resampled.battery_level,"ESM","time","Level",FIGPATH,FIGNAME)
    #&& how about features???
    return resampled
    
if __name__ == "__main__":
    pass