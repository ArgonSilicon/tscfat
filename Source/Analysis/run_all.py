#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 10:29:10 2021

@author: arsi
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import copy

# Local application import
from Source.Analysis.calculate_similarity import calculate_similarity
from Source.Analysis.calculate_novelty import compute_novelty, compute_stability
from Source.Analysis.decompose_timeseries import STL_decomposition#, detect_steps
from Source.Analysis.plot_similarity import plot_similarity
from Source.Analysis.cluster_timeseries import cluster_timeseries
from Source.Analysis.rolling_statistics import rolling_statistics
from Source.Analysis.summary_statistics import summary_statistics

#from arma_model import autocorr
from Source.Analysis.fluctuation_intensity import fluctuation_intensity
from scipy.stats import entropy
#import nolds
import pytest
from Source.Utils.plot_decorator import plot_decorator

#%% LOAD THE DATA FRAME

df_path = Path('/home/arsi/Documents/Data/Combined_data.csv')
df = pd.read_csv(df_path)

df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])
df = df.drop(columns=['date','Other','Work/Study'])

#%% SUMMARY STATISTICS
for name in df.columns.to_list():
    
    SAVENAME = name
    SAVEPATH = Path('/home/arsi/Documents/tscfat/Results/Summary')
    ser = df[name]   
    _ = summary_statistics(ser,"{} summary".format(name), savepath = SAVEPATH, savename = SAVENAME, test = False)

#%% DECOMPOSITION
for name in df.columns.to_list(): 
    ser = df[name]
    SAVEPATH2 = Path('/home/arsi/Documents/tscfat/Results/Decomposition')
    SAVENAME2 = name + '_decomposition'
    _  = STL_decomposition(ser.values,"{} timeseries decomposition".format(name), False, SAVEPATH2, SAVENAME2, ylabel = 'Value', xlabel = 'Date')
    
    
#%% SIMILARITY / NOVELTY / STABILITY
for name in df.columns.to_list():
    ser = df[name]
    SAVEPATH3 = Path('/home/arsi/Documents/tscfat/Results/Similarity')
    SAVENAME3 = name + '_similarity'
    AXIS = None
    sim = calculate_similarity(ser.values.reshape(-1,1))
    stab = compute_stability(sim)
    nov, ker = compute_novelty(sim,edge=7)
    plot_similarity(copy.deepcopy(sim),nov,stab,"{} similarity, novelty, and stability".format(name),SAVEPATH3,SAVENAME3,(0,0.06),0.8,AXIS,ker,False)
    
#%% ROLLING STATISTICS 
for name in df.columns.to_list():
    w = 28
    #ser = df[name].diff(1).diff(7).diff(27).fillna(0)
    ser = df[name]
    FIGPATH = Path('/home/arsi/Documents/tscfat/Results/RollingStatistics')
    FIGNAME = name + '_rolling'
    
    _ = rolling_statistics(ser.to_frame(), w, FIGNAME, FIGPATH)