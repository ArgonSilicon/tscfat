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
from test_status import test_battery_status, test_screen_status

def process_apps(df, df_b, df_s):
    
    # parameters for RQA
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.05 # neigborhood radius
       
    # Load dictionary for app labels
    DICT_PATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
    DICT_NAME = 'labels_dict.json'
    loadname = DICT_PATH / DICT_NAME
    _,labels = load_one_subject(loadname)
    
    #%%
    df['Encoded'] = ordinal_encoding(df['application_name'].values.reshape(-1,1))
    df['group'] = [labels[value] for value in df['application_name'].values]
    df['Encoded_group'] = ordinal_encoding(df['group'].values.reshape(-1,1))
    
    #enc_df = pd.DataFrame(one_hot_encoding(df0['Encoded_group'].values.reshape(-1,4)))
    Colnames = ['Communication','Entertainment','Other','Shop','Social_media','Sports','Travel','Work/Study',]
    enc_df = pd.DataFrame(one_hot_encoding(df['Encoded_group'].values.reshape(-1,1)),columns=Colnames,index=df.index)
    df = pd.concat([df,enc_df], axis=1, join='outer') 
    
    # TODO: fix this for loop
    temp = []
    max_time = pd.Timestamp(min(max(df_b.index.values),max(df_s.index.values)))
    min_time = pd.Timestamp(max(min(df_b.index.values),min(df_s.index.values)))
    
    for i in df.index.values:
        ts = pd.Timestamp(i)
        
        if min_time <= ts <= max_time and all((test_battery_status(df_b,ts),test_screen_status(df_s,ts))):
            temp.append(True)
        else:
            temp.append(False)
    
    df['is_active'] = temp
    
    #df_filt = df.filter(["time",*Colnames])
    df_filt = df[df['is_active'] == True]
    #print(df_filt.shape)
    df_filt = df_filt.filter(['Communication','Entertainment','Other','Shop','Social_media','Sports','Travel','Work/Study',])
    resampled = df_filt.resample("H").sum()
    #resampled = resampled.drop(columns='Other')
    # daily / hours for similarity calulation
    resampled_day = resampled.resample('D').apply(list)
    res = resampled_day[1:-1]
    
    temp = np.zeros((43,8,24))
    for i in range(res.shape[0]):
        temp[i] = np.stack(res.iloc[i].values)
    
    data = temp.reshape(43,-1)
    
    #timeseries = resampled['Encoded_group'].values.reshape(-1,1) # to_numpy() if an array is needed
    timeseries = resampled.filter(['time',*Colnames]).to_numpy()
    
    #%%
    #res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    res, mat = Calculate_RQA(data,ED,TD,RA)
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Similarity/')
    FIGNAME = "Application_usage_similarity"
    sim = calculate_similarity(data,'cosine')
    nov = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Battery level (cosine distance)",FIGPATH,FIGNAME,(0.02,0.06),0.55)
   

    #%% show recursion plot and save figure
    # set correct names and plot title
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_0"
    TITLE = "AppNotifications Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    # set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Metrics/')
    RESNAME = "metrics_0.json"
    dump_to_json(res,RESPATH,RESNAME)  
    
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Timeseries/')
    TSNAME = "timeseries_0.mat"
    save2mat(df['Encoded'].values,TSPATH,TSNAME)        
    
    #% Plot timeseries and save figureShow_recurrence_plot(sim2)
    #FIGNAME = "timeseries_0_scatter"
    #show_timeseries_scatter(df_filt.index,df_filt.Encoded_group,"Application usage","time","Applications",FIGPATH,FIGNAME)
    #show_timeseries_scatter(df_filt.Encoded_group,"Application usage","time","Applications",FIGPATH,FIGNAME)
    #%% Extract features from timeseries, plot, and save
    
    #FIGNAME = "features_0"
    show_features(resampled['Communication'],"Comm","xlab","ylab")
    show_features(resampled['Entertainment'],"Entertainment","xlab","ylab")
    show_features(resampled['Other'],"Other","xlab","ylab")
    show_features(resampled['Sports'],"Sports","xlab","ylab")
    show_features(resampled['Work/Study'],"Work/Study","xlab","ylab")
    show_features(resampled['Shop'],"Shop","xlab","ylab")
    show_features(resampled['Social_media'],"Work/Study","xlab","ylab")
    show_features(resampled['Travel'],"Work/Study","xlab","ylab")
    
    return df, timeseries

if __name__ == "__main__":
    pass