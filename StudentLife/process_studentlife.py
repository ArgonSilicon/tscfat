#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:42:42 2021

@author: arsii
"""

from pathlib import Path

import pandas as pd
import numpy as np
from copy import deepcopy

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
from tscfat.Analysis.cluster_timeseries import cluster_timeseries

#%% LOAD THE DATA
df_path = Path('/home/arsii/Data/StudentLife_cherry_data.csv')
df = pd.read_csv(df_path, index_col=0,parse_dates=True)

#%% LOOP ALL THE SUBJECTS

subjects = ['51','02','12','10','57','35','19','36','17','08']
types = ['activity', 'conversation', 'sleep', 'stress', 'valence','arousal']
c_types = ['activity','conversation']
#%% LOOP ALL THE SUBJECTS AND TYPES

for sub in subjects:
    for typ in types:
        '''       
        # SUMMARY STATISTICS
        print('Processing Summary Statistics: \n')
        
        @process_decorator
        def summary(df,name):
            ser = df[name] 
            _ = summary_statistics(ser,
                                   "Subject: {} Feature: {}".format(sub,typ),
                                   24,
                                   False,
                                   False,
                                   False)
        
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        summary(df_sub,['value'])
        

        print("\nProcessing Rolling Statistics: \n")

        @process_decorator
        def rolling(df,name):
            ser = df[name] 
            _ = rolling_statistics(ser.to_frame(),
                                   24,
                                   doi = None,
                                   savename = False,
                                   savepath = False,
                                   test = False)
            
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        rolling(df_sub,['value'])
        
        

        
        print("\nProcessing Timeseries Decomposition: \n")

        @process_decorator
        def decomposition(df,name):
            ser = df[name].values
    
            # TODO! check additional parameters!
            _ = STL_decomposition(ser,
                                  title = name + '_decomposition',
                                  test = False,
                                  savepath = False,
                                  savename = False,
                                  ylabel = "{} Level".format(name),
                                  xlabel  = "Date",
                                  dates = False,
                                  )
        
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        decomposition(df_sub,['value'])
        
        

        print("\nProcessing Similarity, Noveltym and Stability: \n")

        @process_decorator
        def similarity(df,name):
            ser = df[name].values.reshape(-1,1)
            #ind_s, ind_e = doi2index(doi,df)
    
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
                                title="{} {} Similarity, Novelty and Stability".format(sub,typ),
                                doi = None,
                                savepath = False, 
                                savename = False,
                                ylim = (0,0.05),
                                threshold = 0,
                                axis = None,
                                kernel = kernel,
                                test = False
                                )

        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        similarity(df_sub,['value'])    
    
        '''
       
        print("\nProcessing timeseries plotting: \n")

        @process_decorator
        def plotting(df,name): 
            name = [name]
            _ = plot_timeseries(df,
                                name,
                                title = '{} {}'.format(sub,typ),
                                roll = False, 
                                xlab = "Time", 
                                ylab = "Value", 
                                ylim = False, 
                                savename = False, 
                                savepath = False, 
                                highlight = False, 
                                test=False
                                )
            
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        
        plotting(df_sub,['value'])

#%% CLUSTERING TEST
for sub in subjects:
    for typ in c_types:
        
        print('Processing Timeseries Clustering: \n')

        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        
        df_sub = df_sub.resample('D').apply(list)
        data = np.stack(df_sub.value.values)
        
        clusters = cluster_timeseries(data,
                                      FIGNAME = False,
                                      FIGPATH = False,
                                      title = 'Test', 
                                      n = 5, 
                                      metric = 'DTW', 
                                      highlight = None,
                                      ylim_ = None)
print('Done.')