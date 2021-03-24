#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is the example script for battery level processing. 
The data is loaded in CSV format. 
The analysis is conducted in process_battery_level.py.
The results are stored on disk.

"""
import os
import pandas as pd
from copy import deepcopy

os.chdir('/u/26/ikaheia1/data/Documents/tscfat')  # Provide the new path here

from config import fn, ap, doi

from Source.Analysis.summary_statistics import summary_statistics
from Source.Analysis.rolling_statistics import rolling_statistics
from Source.Analysis.decompose_timeseries import STL_decomposition
from Source.Analysis.calculate_similarity import calculate_similarity
from Source.Analysis.calculate_novelty import compute_novelty, compute_stability
from Source.Analysis.plot_similarity import plot_similarity
from Source.Analysis.plot_timeseries import plot_timeseries
from Source.Utils.doi2int import doi2index


#%% LOAD THE DATA FRAME
df = pd.read_csv(fn.csv_path)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])
df = df.drop(columns=['date','Other','Work/Study'])


# TODO! Put all for loops in one funtion / wrapper
#%% SUMMARY STATISTICS
print('Processing Summary Statistics: \n')

for i, name in enumerate(df.columns.to_list()):        
    print('Column: {:30s} : {}/{}'.format(name,i+1,df.shape[1]))
    ser = df[name] 
    # TODO! add argument names!
    # TODO! fix number of opened figures warning!
    _ = summary_statistics(ser,
                           "{} summary".format(name),
                           ap.summary_window,
                           fn.summary_out,
                           fn.summary_base + name,
                           False)
    

#%% ROLLING STATISTICS 
print("\nProcessing Rolling Statistics: \n")

for i, name in enumerate(df.columns.to_list()):
    print('Column: {:30s} : {}/{}'.format(name,i+1,df.shape[1]))
    ser = df[name] 
    _ = rolling_statistics(ser.to_frame(),
                           ap.rolling_window,
                           doi = doi,
                           savename = fn.rolling_base + name,
                           savepath = fn.rolling_out,
                           test = False)
    
#%% TIMESERIES DECOMPOSITION
print("\nProcessing Timeseries Decomposition: \n")

for i, name in enumerate(df.columns.to_list()):
    print('Column: {:30s} : {}/{}'.format(name,i+1,df.shape[1]))
    ser = df[name].values
    
    # TODO! check additional parameters!
    _ = STL_decomposition(ser,
                          title = name + '_decomposition',
                          test = False,
                          savepath = fn.decomposition_out,
                          savename = fn.decomposition_base + name,
                          ylabel = "{} Level".format(name),
                          xlabel  = "Date",
                          dates = False,
                          )

#%% SIMILARITY, NOVELTY, AND STABILITY
print("\nProcessing Similarity, Noveltym and Stability: \n")

for i, name in enumerate(df.columns.to_list()):
    print('Column: {:30s} : {}/{}'.format(name,i+1,df.shape[1]))
    ser = df[name].values.reshape(-1,1)
    
    ind_s, ind_e = doi2index(doi,df)
    
    # TODO! check todos in plot_similarity.py
    # TODO! How to fix x-axis labels?
    # TODO! Check additional parameters
    # TODO! How to calculate threshold?
    
    sim = calculate_similarity(ser)
    stab = compute_stability(sim)
    nov, kernel = compute_novelty(sim,edge=7)
    _ = plot_similarity(deepcopy(sim),
                        nov,
                        stab,
                        title="{} Similarity, Novelty and Stability".format(name),
                        doi = (ind_s,ind_e),
                        savepath = fn.similarity_out, 
                        savename = fn.similarity_base + name,
                        ylim = (0,0.05),
                        threshold = 0,
                        axis = None,
                        kernel = kernel,
                        test = False
                        )
    
#%% CLUSTERING
print("\nProcessing timeseries clustering: \n")

for i, name in enumerate(df.columns.to_list()):
    print('Column: {:30s} : {}/{}'.format(name , i+1, df.shape[1]))
    
#%% PLOTTING TIMESERIES
print("\nProcessing timeseries plotting: \n")

for i, name in enumerate(ap.plot_cols):
    
    print('Columns: {:60s} : {}/{}'.format(" - ".join(name), i+1, len(ap.plot_cols)))
    
    _ = plot_timeseries(df,
                        name,
                        title = fn.plotting_base + '_'.join(name),
                        roll = False, 
                        xlab = "Time", 
                        ylab = "Value", 
                        ylim = False, 
                        savename = fn.plotting_base + '_'.join(name), 
                        savepath = fn.plotting_out, 
                        highlight = False, 
                        test=False
                        )
