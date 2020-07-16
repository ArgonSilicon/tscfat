#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 13:24:55 2020

@author: ikaheia1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from decompose_timeseries import STL_decomposition
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from Plot_similarity import Plot_similarity
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
from plot_timeseries import show_features
from vector_encoding import custom_resampler


#%%
time        = np.arange(0, 1344, 1);
amplitude   = 2*np.abs(np.sin(2*np.pi*(1/48)*time)) \
                + 1*np.abs(np.sin(2*np.pi*(1/(7*48))*time)) \
                + 1*np.abs(np.sin(2*np.pi*(1/(4*7*48))*time)) \
                + 1*np.abs(np.random.normal(0,1,len(time))) \
                + np.exp(time/1000) 

time_2 = np.arange(0,50,1);
amplitude_2 = 10*np.abs(np.sin(2*np.pi*(1/100)*time_2))

amplitude[100:400] -= 0.6*np.abs(np.random.normal(0,1,300))
amplitude[150:350] -= 0.8*np.abs(np.random.normal(0,1,200))
amplitude[200:300] -= 1*np.abs(np.random.normal(0,1,100))
amplitude[250:300] -= 2*np.abs(np.random.normal(0,1,50))
amplitude[700:1000] += 1*np.abs(np.random.normal(0,1,300))
amplitude[900:1100] += 1*np.abs(np.random.normal(0,1,200))
amplitude[1000:1100] += 2*np.abs(np.random.normal(0,1,100))
amplitude[1100:1344] -= 2*np.abs(np.random.normal(0,1,244))
amplitude[1200:1344] -= 4*np.abs(np.random.normal(0,1,144))
amplitude[525:575] += amplitude_2

#%%
decomposition = STL_decomposition(amplitude)

#%%
FIGPATH = False
FIGNAME = False
sim = calculate_similarity(amplitude.reshape(-1,1),'euclidean')
nov = compute_novelty_SSM(sim,L=24)
Plot_similarity(sim,nov,"Similarity and novelty",FIGPATH,FIGNAME)

#%%
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.1 # neigborhood radius
    
# Calculate recursion plot and metrix
res, mat = Calculate_RQA(ts2,ED,TD,RA)
res, mat = Calculate_RQA(amplitude.reshape(-1,1),ED,TD,RA)

    
#%% show recursion plot and save figure
TITLE = "Test recurrence plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)

#%%
dr = pd.date_range(start='1/1/2018', periods=1344, freq='H')
series = pd.Series(amplitude,index=dr)
show_features(series,"Test features","xlab","ylab",(24*7),1,'right',False,FIGPATH,FIGNAME)

###############################################################################
#%% test trend only
amplitude_trend = decomposition.trend.reshape(-1,1)

#%%
sim = calculate_similarity(amplitude_trend,'euclidean')
nov = compute_novelty_SSM(sim,L=24*7)
Plot_similarity(sim,nov,"Similarity and novelty",FIGPATH,FIGNAME)
#%%
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.50 # neigborhood radius
    
#%% Calculate recursion plot and metrix
res, mat = Calculate_RQA(amplitude_trend,ED,TD,RA)
    
#%% show recursion plot and save figure
TITLE = "Test recurrence plot: trend only \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)

#%%
dr = pd.date_range(start='1/1/2018', periods=1344, freq='H')
series = pd.Series(amplitude_trend.reshape(-1),index=dr)
show_features(series,"Test features: trend only","xlab","ylab",24,1,'right',False,FIGPATH,FIGNAME)

###############################################################################
#%% test detrended values
amplitude_detrend = decomposition.observed.reshape(-1,1) - decomposition.trend.reshape(-1,1)

#%%
sim = calculate_similarity(amplitude_detrend,'euclidean')
nov = compute_novelty_SSM(sim,L=24*7)
Plot_similarity(sim,nov,"Similarity and novelty",FIGPATH,FIGNAME)
#%%
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.50 # neigborhood radius
    
#%% Calculate recursion plot and metrix
res, mat = Calculate_RQA(amplitude_detrend,ED,TD,RA)
    
#%% show recursion plot and save figure
TITLE = "Test recurrence plot: detrended \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)

#%%
dr = pd.date_range(start='1/1/2018', periods=1344, freq='H')
series = pd.Series(amplitude_trend.reshape(-1),index=dr)
show_features(series,"Test features: detrended ","xlab","ylab",24,1,'right',False,FIGPATH,FIGNAME)

#%% test resampling / 1D
resampled = series.resample('D').apply(custom_resampler)
timeseries = resampled.values
timeseries = np.stack(timeseries)
#timeseries = np.stack(timeseries[1:-1])

#%%
sim = calculate_similarity(timeseries,'euclidean')
nov = compute_novelty_SSM(sim,L=7)
Plot_similarity(sim,nov,"Similarity and novelty",FIGPATH,FIGNAME)
#%%
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.15 # neigborhood radius
    
#%% Calculate recursion plot and metrix
res, mat = Calculate_RQA(amplitude_detrend,ED,TD,RA)

#%% show recursion plot and save figure
TITLE = "Test recurrence plot: resampled \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)

