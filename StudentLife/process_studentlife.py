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
n_types = ['sleep', 'stress', 'valence','arousal']
c_types = ['activity','conversation']
#%% LOOP ALL THE SUBJECTS AND TYPES

doi = (2013,4,15),(2013,4,26)
ind_s, ind_e = doi2index(doi,df)

for sub in subjects:
    for typ in n_types:
        '''    
        # SUMMARY STATISTICS
        print('Processing Summary Statistics: \n')
        
        @process_decorator
        def summary(df,name):
            ser = df[name] 
            _ = summary_statistics(ser,
                                   title = "Subject: {} Feature: {}".format(sub,typ),
                                   window = 14,
                                   savepath = Path('/home/arsii/tscfat/StudentLife/Results/Summary'),
                                   savename = 'Summary_{}_{}'.format(typ,sub),
                                   test = False)
        
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        summary(df_sub,['value'])
        

        print("\nProcessing Rolling Statistics: \n")

        
        @process_decorator
        def rolling(df,name):
            ser = df[name] 
            _ = rolling_statistics(ser.to_frame(),
                                   14,
                                   doi = doi,
                                   savepath = Path('/home/arsii/tscfat/StudentLife/Results/RollingStatistics'),
                                   savename = 'Rolling_{}_{}'.format(typ,sub),
                                   test = False)
            
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        rolling(df_sub,['value'])
        
        

        
        print("\nProcessing Timeseries Decomposition: \n")

        @process_decorator
        def decomposition(df,name):
            ser = df[name].values
    
            # TODO! check additional parameters!
            # TODO! check dates!!!???
            _ = STL_decomposition(ser,
                                  title = name + '_decomposition',
                                  test = False,
                                  savepath = Path('/home/arsii/tscfat/StudentLife/Results/Decomposition'),
                                  savename = 'Decomposition_{}_{}'.format(typ,sub),
                                  ylabel = "{} Level".format(name),
                                  xlabel  = "Date",
                                  dates = False,
                                  )
        
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        decomposition(df_sub,['value'])
        
        

        print("\nProcessing Similarity, Noveltym and Stability: \n")

        index = pd.date_range('2013-03-27', '2013-06-01', freq='H')
        
        @process_decorator
        def similarity(df,name):
            ser = df[name].values.reshape(-1,1)
            #ind_s, ind_e = doi2index(doi,df)
    
            # TODO! check todos in plot_similarity.py
            # TODO! How to fix x-axis labels?
            # TODO! Check additional parameters
            # TODO! How to calculate threshold?
            
            sim = calculate_similarity(ser)
            print(sim)
            stab = compute_stability(sim)
            print(stab)
            nov, kernel = compute_novelty(sim,edge=7)
            print(nov)
            _ = plot_similarity(deepcopy(sim),
                                nov,
                                stab,
                                title="{} {} Similarity, Novelty and Stability".format(sub,typ),
                                doi = (ind_s, ind_e),
                                savepath = Path('/home/arsii/tscfat/StudentLife/Results/Similarity'),
                                savename = 'Similarity_{}_{}'.format(typ,sub),
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
                                roll = 14, 
                                xlab = "Time", 
                                ylab = "Value", 
                                ylim = False, 
                                savepath = Path('/home/arsii/tscfat/StudentLife/Results/Timeseries'),
                                savename = 'Timeseries_{}_{}'.format(typ,sub), 
                                highlight = (ind_s, ind_e),
                                test = False
                                )
            
        df_sub = df[(df['id'] == int(sub)) & (df['type'] == typ)]
        
        plotting(df_sub,['value'])
        
