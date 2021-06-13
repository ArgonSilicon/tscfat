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

from config import fn, ap, doi

from tscfat.Analysis.summary_statistics import summary_statistics
from tscfat.Analysis.rolling_statistics import rolling_statistics
from tscfat.Analysis.decompose_timeseries import STL_decomposition
from tscfat.Analysis.calculate_similarity import calculate_similarity
from tscfat.Analysis.calculate_novelty import compute_novelty
from tscfat.Analysis.calculate_stability import compute_stability
from tscfat.Analysis.plot_similarity import plot_similarity
from tscfat.Analysis.plot_timeseries import plot_timeseries
from tscfat.Utils.doi2int import doi2index
from tscfat.Utils.process_decorator import process_decorator


#%% LOAD THE DATA FRAME
df = pd.read_csv(fn.csv_path)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])
df = df.drop(columns=['date'])
cols = df.columns.to_list()
#TODO! please remove this!
df.index = df.index.shift(200,freq='D')

#%% SUMMARY STATISTICS   
print('Processing Summary Statistics: \n')

@process_decorator
def summary(df,name):
    ser = df[name] 
    _ = summary_statistics(ser,
                           doi,
                           title = 'Summary statistics: Average resting HR',
                           window = 14,
                           savepath = False,
                           savename = False,
                           test = False)
    
summary(df,cols)

'''
@process_decorator
def summary(df,name):
    ser = df[name] 
    _ = summary_statistics(ser,
                           doi,
                           fn.summary_base + name,
                           ap.summary_window,
                           fn.summary_out,
                           fn.summary_base + name,
                           test = False)

summary(df,cols)
'''

#%% ROLLING STATISTICS 
print("\nProcessing Rolling Statistics: \n")

@process_decorator
def rolling(df,name):
    ser = df[name] 
    _ = rolling_statistics(ser.to_frame(),
                           ap.rolling_window,
                           doi = doi,
                           savename = False,
                           savepath = False,
                           test = False)

rolling(df,cols)


'''
@process_decorator
def rolling(df,name):
    ser = df[name] 
    _ = rolling_statistics(ser.to_frame(),
                           ap.rolling_window,
                           doi = doi,
                           savename = fn.rolling_base + name,
                           savepath = fn.rolling_out,
                           test = False)

rolling(df,cols)
'''

#%% TIMESERIES DECOMPOSITION
print("\nProcessing Timeseries Decomposition: \n")
ind_s, ind_e = doi2index(doi,df)

@process_decorator
def decomposition(df,name):
    ser = df[name].values
     
    # TODO! check additional parameters!
    # TODO! add doi
    _ = STL_decomposition(ser,
                          title = 'Time series decomposition: negative',
                          test = False,
                          savepath = False,
                          savename = False,
                          ylabel = "{} Level".format(name),
                          xlabel  = "Day",
                          dates = False,
                          doi = (ind_s,ind_e),
                          )

decomposition(df,cols)

'''
@process_decorator
def decomposition(df,name):
    ser = df[name].values
     
    # TODO! check additional parameters!
    # TODO! add doi
    _ = STL_decomposition(ser,
                          title = name + '_decomposition',
                          test = False,
                          savepath = fn.decomposition_out,
                          savename = fn.decomposition_base + name,
                          ylabel = "{} Level".format(name),
                          xlabel  = "Date",
                          dates = False,
                          doi = (ind_s,ind_e),
                          )

decomposition(df,cols)
'''

#%% SIMILARITY, NOVELTY, AND STABILITY
print("\nProcessing Similarity, Noveltym and Stability: \n")

@process_decorator
def similarity(df,name):
    ser = df[name].values.reshape(-1,1)
    ind_s, ind_e = doi2index(doi,df)
    
    # TODO! check todos in plot_similarity.py
    # TODO! How to fix x-axis labels?
    # TODO! Check additional parameters
    # TODO! How to calculate threshold?
    
    sim = calculate_similarity(ser)
    stab = compute_stability(sim,edge=14)
    nov, kernel = compute_novelty(sim,edge=14)
    _ = plot_similarity(deepcopy(sim),
                        nov,
                        stab,
                        title="{} Similarity, Novelty and Stability".format(name),
                        doi = (ind_s,ind_e),
                        #savepath = fn.similarity_out,
                        savepath = False,
                        #savename = fn.similarity_base + name,
                        savename = False,
                        ylim = (0,0.05),
                        threshold = 0.9,
                        axis = None,
                        kernel = kernel,
                        test = False,
                        )

similarity(df,cols)    
    
#%% PLOTTING TIMESERIES
print("\nProcessing timeseries plotting: \n")
    
@process_decorator
def plotting(df,name): 
    doi = ((2011, 10, 1), (2011, 12, 24))
    _ = plot_timeseries(df,
                        name,
                        title = 'Rolling window average: positive, negative, screen activations',
                        roll = 28, 
                        xlab = "Date", 
                        ylab = "Value", 
                        ylim = False,
                        savename = False, 
                        savepath = False,
                        highlight = doi, 
                        test=False
                        )
    
plotting(df,ap.plot_cols)

'''
@process_decorator
def plotting(df,name): 
    ind_s, ind_e = doi2index(doi,df)
    _ = plot_timeseries(df,
                        name,
                        title = fn.plotting_base + '_'.join(name),
                        roll = 7, 
                        xlab = "Date", 
                        ylab = "Value", 
                        ylim = False,
                        savename = fn.plotting_base + '_'.join(name), 
                        savepath = fn.plotting_out,
                        highlight = (ind_s,ind_e), 
                        test=False
                        )
    
plotting(df,ap.plot_cols)
'''