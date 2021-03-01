#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi

- Plot timeseries decomposition
- Plot similarity and novelty
- Plot rolling stats
- Plot clustering

"""

# standard library imports
from pathlib import Path
import copy

# third party imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Local application import
from Source.Analysis.calculate_similarity import calculate_similarity
from Source.Analysis.calculate_novelty import compute_novelty
from Source.Analysis.decompose_timeseries import STL_decomposition#, detect_steps
from Source.Analysis.plot_similarity import plot_similarity
from Source.Analysis.cluster_timeseries import cluster_timeseries
from Source.Analysis.rolling_statistics import rolling_statistics
from Source.Analysis.summary_statistics import summary_statistics

plt.style.use('seaborn')

def process_battery(df,FIGPATH):
    
    #%% filter dataframe and resample hourly means
    df_filt = df.filter(["time","battery_level",])
    df_grouped_lists = df_filt.battery_level.groupby(df_filt.index.hour).apply(list) # -> for grouped_histograms()
    resampled = df_filt.resample("H").mean()
    
    missing_values = resampled.isna()
    resampled_interpolated = resampled.interpolate('linear') 
    timeseries = resampled_interpolated.values
    
    
    # daily / hours for similarity calulation
    resampled_day = resampled_interpolated.resample('D').apply(list)
    data = np.stack(resampled_day.battery_level.values[1:-1])
    #%%
    _ = summary_statistics(resampled_interpolated.battery_level,"Time series summary",False,False)
    
    #%% Plot timeseries decompostition and distribution for each component
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Decomposition')
    #FIGPATH = Path(r'F:\tscfat\Results\Decomposition') 
    FIGPATH = Path.cwd() / 'Results' / 'Decomposition' 
    #FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat/Results/Decomposition')
    FIGNAME = "Battery_level_rolling_statistics" 
    _  = STL_decomposition(timeseries,"Battery level timeseries decomposition", False, FIGPATH,FIGNAME)
       
    #%% rolling stats
    w = 7*24
    w=7
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\RollingStatistics')
    #FIGPATH = Path(r'F:\tscfat\Results\RollingStatistics')
    FIGPATH = Path.cwd() / 'Results' / 'RollingStatistics'
    #FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat/Results/RollingStatistics')
    FIGNAME = "Battery_level_Rolling_Statistics"
    
    _ = rolling_statistics(resampled_interpolated,w,FIGNAME,FIGPATH)
    
    
    #%% calculate similarity and novelty
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Similarity')
    #FIGPATH = Path(r'F:\tscfat\Results\Similarity')
    FIGPATH = Path.cwd() / 'Results' / 'Similarity'
    #FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat/Results/Similarity')
    FIGNAME = "Battery_level_similarity"
    AXIS = None #resampled_day[1:-1].index.strftime('%m-%d')
    
    sim = calculate_similarity(data)
    #sim = calculate_similarity(data)
    stab = compute_stability(sim)
    nov, kernel = compute_novelty(sim,edge=7)
    plot_similarity(copy.deepcopy(sim),nov,"Battery level (euclidean distance)",FIGPATH,FIGNAME,(0,0.06),0.8,AXIS,kernel)

    #%%
    # Timeseries clustering
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Clusters')
    #FIGPATH = Path(r'F:\tscfat\Results\Clusters')
    FIGPATH = Path.cwd() / 'Results' / 'Clusters'
    #FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat/Results/Clusters')
    FIGNAME = "Clustered_timeseries"
    
    clusters = cluster_timeseries(data,FIGNAME, FIGPATH, title="Battery level clustered timeseries",n=3)

    filt_1 = clusters == 0
    filt_2 = clusters == 1
    filt_3 = clusters == 2
    #filt_4 = clusters == 3
    
    clust_1 = data[filt_1]
    clust_2 = data[filt_2]
    clust_3 = data[filt_3]
    #clust_4 = data[filt_4]
    
    fig,ax = plt.subplots(3,1,figsize=(10,7))
    fig.suptitle("Battery level clusters / hourly average",fontsize=20)
    
    ax[0].plot(np.mean(clust_1,axis=0))
    ax[0].set_title('Clusters 1')
    ax[0].set(xlabel = "Time (Hour)",ylabel="Battery level (%)")
    ax[0].set(ylim=(30,100))
    
        
    ax[1].plot(np.mean(clust_2,axis=0))
    ax[1].set_title("Cluster 2")
    ax[1].set(xlabel = "Time (Hour)",ylabel="Battery level (%)")
    ax[1].set(ylim=(30,100))
    
    
    ax[2].plot(np.mean(clust_3,axis=0))
    ax[2].set_title("Cluster 3")
    ax[2].set(xlabel = "Time (Hour)",ylabel="Battery level (%)")
    ax[2].set(ylim=(30,100))
    
    '''
    ax[3].plot(np.mean(clust_4,axis=0))
    ax[3].set_title("Cluster 3")
    ax[3].set(xlabel = "Time (Hour)",ylabel="Battery level (%)")
    ax[3].set(ylim=(30,100))
    '''
    
    
    fig.tight_layout(pad=1.0)
    
    plt.show()
    
    weekdays = pd.DataFrame(data = clusters,    # values
                            index = resampled_day[1:-1].index,   # 1st column as index
                            columns = ['clusters']) # 1st row as the column names
    
    wd1 = weekdays[weekdays['clusters'] == 0]
    wd1['date'] = wd1.index
    wd1['date'] = pd.to_datetime(wd1['date'])
    
    wd = weekdays.groupby(wd1['date'].dt.day_name()).count()
    wd.index = pd.Categorical(wd.index, categories= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                           ordered=True)
    wd = wd.sort_index()
    wd.plot(kind='bar',title="Cluster 0 / daily counts",ylabel='Count')
    
    wd2 = weekdays[weekdays['clusters'] == 1]
    wd2['date'] = wd2.index
    wd2['date'] = pd.to_datetime(wd2['date'])
    
    wd3 = weekdays.groupby(wd2['date'].dt.day_name()).count()
    wd3.index = pd.Categorical(wd3.index, categories= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                           ordered=True)
    wd3 = wd3.sort_index()
    wd3.plot(kind='bar',title="Cluster 1 / daily counts",ylabel='Count')
    
    wd4 = weekdays[weekdays['clusters'] == 2]
    wd4['date'] = wd4.index
    wd4['date'] = pd.to_datetime(wd4['date'])
    
    wd5 = weekdays.groupby(wd4['date'].dt.day_name()).count()
    wd5.index = pd.Categorical(wd5.index, categories= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                           ordered=True)
    wd5 = wd5.sort_index()
    wd5.plot(kind='bar',title="Cluster 2 / daily counts",ylabel='Count')
        
    fig,ax = plt.subplots(figsize=[10,4])
    weekdays.plot(style='o',ax=ax)
    ax.set_yticks([0,1,2])
    ax.set(title='Battery level clustered time series',ylabel='Cluster')
    ax.set(ylim=(-1,3))
    plt.show()
    
    #%%
    
    fig,ax = plt.subplots(2,1,figsize=(10,7))
    fig.suptitle("Cluster weekday distribution",fontsize=20)
    
    wd.plot(kind='bar',ax = ax[0])
    ax[0].set_title('Clusters 0')
    ax[0].set(xlabel = "Weekday",ylabel="Count")
    ax[0].set(ylim=(0,35))
    
        
    wd3.plot(kind='bar',ax = ax[1])
    ax[1].set_title("Cluster 1")
    ax[1].set(xlabel = "Weekday",ylabel="Count")
    ax[1].set(ylim=(0,35))
    fig.tight_layout(pad=1.0)
    
    plt.show()
    #%%
    return df, timeseries, data

if __name__ == "__main__":
    pass