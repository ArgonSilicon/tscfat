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
from matplotlib.dates import DateFormatter
from arma import arma, autocorr
from datetime import datetime

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
    DICT_PATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Data/')
    DICT_NAME = 'labels_dict.json'
    loadname = DICT_PATH / DICT_NAME
    
    #_,labels = load_one_subject(loadname)
    with open(loadname) as json_file: 
        labels = json.load(json_file) 
    #%%
    df['Encoded'] = ordinal_encoding(df['application_name'].values.reshape(-1,1))
    df['group'] = [labels[value] for value in df['application_name'].values]
    df['Encoded_group'] = ordinal_encoding(df['group'].values.reshape(-1,1))
    
    #enc_df = pd.DataFrame(one_hot_encoding(df0['Encoded_group'].values.reshape(-1,4)))
    Colnames = ['Communication','Entertainment','Other','Shop','Social_media','Sports','Transportation','Travel','Work/Study',]
    enc_df = pd.DataFrame(one_hot_encoding(df['Encoded_group'].values.reshape(-1,1)),columns=Colnames,index=df.index)
    df = pd.concat([df,enc_df], axis=1, join='outer') 
    
    # TODO: fix this for loop
    temp = []
    max_time = pd.Timestamp(min(max(df_b.index.values),max(df_s.index.values)))
    min_time = pd.Timestamp(max(min(df_b.index.values),min(df_s.index.values)))
    
    df_b = df_b.sort_index()
    df_s = df_s.sort_index()
    
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
    df_filt = df_filt.filter(['Communication','Entertainment','Other','Shop','Social_media','Sports','Transportation','Travel','Work/Study',])
    resampled = df_filt.resample("H").sum()
    #resampled = resampled.drop(columns='Other')
    # daily / hours for similarity calulation
    resampled_day = resampled.resample('D').apply(list)
    res = resampled_day[1:-1]
    
    temp2 = np.zeros((68,9,24))
    for i in range(res.shape[0]):
        temp2[i] = np.stack(res.iloc[i].values)
    
    data = temp2.reshape(68,-1)
    
    #timeseries = resampled['Encoded_group'].values.reshape(-1,1) # to_numpy() if an array is needed
    timeseries = resampled.filter(['time',*Colnames]).to_numpy()
    
    #%%
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    '''
    res, mat = Calculate_RQA(data,ED,TD,RA)
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Similarity/')
    FIGNAME = "Application_usage_similarity"
    sim = calculate_similarity(data,'cosine')
    nov = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Application usage (cosine distance)",FIGPATH,FIGNAME,(0.02,0.06),0.55)
    '''

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
    show_features(resampled['Transportation'],"Transportation","xlab","ylab")
   
    #%%
    df_a = df[df['is_active'] == True]
    df_f = df_a.filter(['Communication', 'Entertainment', 'Other', 'Shop', 'Social_media',
       'Sports', 'Transportation','Travel', 'Work/Study'])

    df_d = df_f.resample('D').sum()
    df_d_rowsum = df_d.sum(axis=1)
    df_p = df_d.loc[:,"Communication":"Work/Study"].div(df_d_rowsum.values, axis=0)
    
    #%% plot stuff
    date_form = DateFormatter("%m-%d")
       
    fig,ax = plt.subplots(5,2,figsize=(12,15))
    fig.suptitle("App notifications",fontsize=20,y=1.02)
    
    ax[0,0].plot(df_d['Communication'])
    ax[0,0].set_title('Communication',fontsize=16)
    ax[0,0].set_xlabel('Time (d)')
    ax[0,0].set_ylabel('Value')
    #ax[0,0].set_ylim(1,6)
    ax[0,0].xaxis.set_major_formatter(date_form)
       
    ax[0,1].plot(df_d['Entertainment'])
    ax[0,1].set_title('Entertainment',fontsize=16)
    ax[0,1].set_xlabel('Time (d)')
    ax[0,1].set_ylabel('Value')
    #ax[0,1].set_ylim(1,6)
    ax[0,1].xaxis.set_major_formatter(date_form)
    
    ax[1,0].plot(df_d['Other'])
    ax[1,0].set_title('Other',fontsize=16)
    ax[1,0].set_xlabel('Time (d)')
    ax[1,0].set_ylabel('Value')
    #ax[1,0].set_ylim(1,6)
    ax[1,0].xaxis.set_major_formatter(date_form)
    
    ax[1,1].plot(df_d['Shop'])
    ax[1,1].set_title('Shop',fontsize=16)
    ax[1,1].set_xlabel('Time (d)')
    ax[1,1].set_ylabel('Value')
    #ax[1,1].set_ylim(1,6)
    ax[1,1].xaxis.set_major_formatter(date_form)
    
    ax[2,0].plot(df_d['Social_media'])
    ax[2,0].set_title('Social_media',fontsize=16)
    ax[2,0].set_xlabel('Time (d)')
    ax[2,0].set_ylabel('Value')
    #ax[2,0].set_ylim(1,6)
    ax[2,0].xaxis.set_major_formatter(date_form)
    
    ax[2,1].plot(df_d['Sports'])
    ax[2,1].set_title('Sports',fontsize=16)
    ax[2,1].set_xlabel('Time (d)')
    ax[2,1].set_ylabel('Value')
    #ax[2,1].set_ylim(1,6)
    ax[2,1].xaxis.set_major_formatter(date_form)
    
    ax[3,0].plot(df_d['Travel'])
    ax[3,0].set_title('Travel',fontsize=16)
    ax[3,0].set_xlabel('Time (d)')
    ax[3,0].set_ylabel('Value')
    #ax[3,0].set_ylim(1,6)
    ax[3,0].xaxis.set_major_formatter(date_form)
    
    ax[3,1].plot(df_d['Work/Study'])
    ax[3,1].set_title('Work/Study',fontsize=16)
    ax[3,1].set_xlabel('Time (d)')
    ax[3,1].set_ylabel('Value')
    #ax[3,1].set_ylim(1,6)
    ax[3,1].xaxis.set_major_formatter(date_form)
    
    ax[4,0].plot(df_d['Transportation'])
    ax[4,0].set_title('Transportation',fontsize=16)
    ax[4,0].set_xlabel('Time (d)')
    ax[4,0].set_ylabel('Value')
    #ax[3,1].set_ylim(1,6)
    ax[4,0].xaxis.set_major_formatter(date_form)
    
    fig.tight_layout(pad=1.0)
    plt.show()
    
    #%% Bar Plots
    
    fig = plt.figure(figsize=(8.3,5))
    barWidth = 0.95
    r = df_p.index
    # Create green Bars
    plt.bar(r, df_p['Communication'], color='#0571b0', edgecolor='white', width=barWidth,label="Communication")
    # Create orange Bars
    plt.bar(r, df_p['Entertainment'], bottom=df_p['Communication'], color='#f4a582', edgecolor='white', width=barWidth,label="Entertainment")
    # Create blue Bars
    plt.bar(r, df_p['Other'], bottom=[i+j for i,j in zip(df_p['Communication'],df_p['Entertainment'] )], color='#92c5de', edgecolor='white', width=barWidth,label="Other")
    # Create red bars
    plt.bar(r, df_p['Sports'], bottom=[i+j+k for i,j,k in zip(df_p['Communication'],df_p['Entertainment'],df_p['Other'])], color='#ca0020', edgecolor='white', width=barWidth,label="Sports")
    # Create yellow bars
    plt.bar(r, df_p['Work/Study'], bottom=[i+j+k+l for i,j,k,l in zip(df_p['Communication'],df_p['Entertainment'],df_p['Other'],df_p['Sports'])], color='#dddddd', edgecolor='white', width=barWidth,label="Work/Study")
    #plt.legend(fontsize=14)
    plt.legend(title='Legend', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=14)
    plt.title("Application usage proportions",fontsize=24,y=1.02)
    plt.ylabel("Proportion",fontsize=16)
    plt.xlabel('Time (Date)',fontsize=16)
    plt.show()
    #%% Plot all apps
    all_sums = df_d.sum(axis=1)
    all_roll = all_sums.rolling(7).mean()
    all_var = all_sums.rolling(7).var()
    all_auto = all_sums.rolling(7).apply(autocorr)
    
    #%%
    
    fig = plt.figure(figsize=(8.3,6))
    
    plt.suptitle('App notification daily sums and extracted features',fontsize=20,y=1.03)
    
    plt.subplot(2,2,1)
    
    all_sums.plot()
    plt.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")    
    plt.title("App notification total count")
    plt.ylabel("Total count")
    plt.xlabel('')
    #plt.show()
    
    plt.subplot(2,2,2)

    all_roll.plot()
    plt.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")    
    plt.title("App notification rolling(7) mean")
    plt.ylabel("Averaged total count")
    plt.xlabel('')
    #plt.show()
    
    plt.subplot(2,2,3)
    all_var.plot()
    plt.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")
    plt.title("App notification rolling(7) variance")
    plt.ylabel("Variance")
    plt.xlabel("Time (date)")
    #plt.show()
    
    plt.subplot(2,2,4)
    all_auto.plot()
    plt.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")
    plt.title("App notifation rolling(7) autocorrelation(1)")
    plt.ylabel("Autocorrelation")
    plt.xlabel("Time (date)")
    
    fig.tight_layout(pad=1.3)

    #%%
    return df, timeseries

if __name__ == "__main__":
    pass