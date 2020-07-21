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
from scipy import signal

# Local application import


from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler, normalize_values
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
from save_results import dump_to_json
from plot_timeseries import show_timeseries_scatter, show_timeseries_line, show_features
from save2mat import save2mat
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from decompose_timeseries import STL_decomposition
from Plot_similarity import Plot_similarity
from interpolate_missing import interpolate_missing


def process_battery(df):
    
    #%% Recursion plot settings
    ED = 1 # embedding dimensions
    TD = 1 # time delay
    RA = 0.5 # neigborhood radius
    
    #%% filter dataframe and resample hourly means
    df_filt = df.filter(["time","battery_level",])
    resampled = df_filt.resample("H").mean()
    resampled_interpolated, _ = interpolate_missing(resampled,'linear')
    timeseries = resampled_interpolated.values
   
    #%% timeseries decompostition
    
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/SL_2/Decomposition/')
    FIGNAME = "decomposition" 
    decomp = STL_decomposition(timeseries,FIGPATH,FIGNAME)
    
    #%%
    from scipy import signal
    
    sig = decomp.resid.reshape(-1,1)
    
    sig = timeseries.reshape(-1,1)

    x = np.linspace(-2,2,51)

    #win = np.sinc(x).reshape(-1,1)
    
    win = signal.hann(50).reshape(-1,1)
    
    win = np.gradient(win,axis=0)
    
    win = win - win.mean()
    
    win = win / win.max()
    
    filtered = signal.convolve(sig, win, mode='same') / sum(win)
    
    from scipy.signal import find_peaks

    peaks, properties = find_peaks(filtered.reshape(-1), height=0)
    
    bottoms, properties_b = find_peaks(-filtered.reshape(-1),height=0)
    
    heights = properties['peak_heights']
    
    lows = properties_b['peak_heights']
    
    
    top_indices = heights.argsort()[-5:][::-1]
    
    top_peaks = peaks[top_indices]
    
    
    neg_indices = (lows).argsort()[-5:][::-1]
    
    neg_peaks = bottoms[neg_indices]

    #plt.plot(x)

    #plt.plot(peaks, x[peaks], "x")

    #plt.plot(np.zeros_like(x), "--", color="gray")

    #plt.show()



    import matplotlib.pyplot as plt

    fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True)

    ax_orig.plot(sig)

    ax_orig.set_title('Original pulse')

    ax_orig.margins(0, 0.1)

    ax_win.plot(win)

    ax_win.set_title('Filter impulse response')

    ax_win.margins(0, 0.1)

    ax_filt.plot(filtered)
    
    #ax_filt.plot(bottoms, filtered[bottoms], "x")
    
    ax_filt.plot(neg_peaks, filtered[neg_peaks], "x", color="blue")
    
    ax_filt.plot(top_peaks, filtered[top_peaks], "x", color="red")
    
    #ax_filt.vlines(tuple(top_peaks),-1, 1, color = "red")
    
    #plt.vlines(x = 954, ymin=-1, ymax=1, color = "C1")

    ax_filt.set_title('Filtered signal')

    ax_filt.margins(0, 0.1)

    fig.tight_layout()

    fig.show()
    
    high_ts = resampled_interpolated.index[peaks[top_indices]]
    
    low_ts = resampled_interpolated.index[bottoms[neg_indices]]
    
    #%% calculate receursion plot and metrics
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
        
    #%% show recursion plot and save figure
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_1"
    TITLE = "Battery level Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
   
    #%% Recursion on trend
    res, mat = Calculate_RQA(decomp.trend.reshape(-1,1), ED,TD,RA)
    
    FIGNAME = "recplot_1_trend"
    TITLE = "Battery level Recurrence Plot / Trend \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    #%% calculate similarity and novelty
    sim = calculate_similarity(timeseries,'euclidean')
    nov = compute_novelty_SSM(sim,L=24)
    Plot_similarity(sim,nov)
    
    # set correct names and save metrics as json 
    RESPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Metrics/')
    RESNAME = "metrics_1.json"
    dump_to_json(res,RESPATH,RESNAME)   
    
    # save the timeseries
    TSPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Timeseries/')
    TSNAME = "timeseries_1.mat"
    save2mat(timeseries,TSPATH,TSNAME)
    
    NPNAME = "timeseries_1.npy"
    with open(FIGPATH / NPNAME, mode="wb") as outfile:
        np.save(outfile,timeseries)       
    
    #%% Plot timeseries and save figure
    FIGNAME = "timeseries_1_scatter"
    show_timeseries_scatter(resampled_interpolated['battery_level'],"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "timeseries_1_line"
    show_timeseries_line(resampled_interpolated['battery_level'],"Battery level / hourly mean","time","Level",FIGPATH,FIGNAME)
    #%% Extract features from timeseries, plot, and save
    show_features(resampled_interpolated['battery_level'],"Battery level","xlab","ylab",window=24)
    


    return df

if __name__ == "__main__":
    pass