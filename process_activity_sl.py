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
import matplotlib.pyplot as plt

# third party imports
import numpy as np

# Local application import
from tscfat.Analysis.calculate_similarity import calculate_similarity
from tscfat.Analysis.calculate_novelty import compute_novelty
from tscfat.Analysis.decompose_timeseries import STL_decomposition#, detect_steps
from tscfat.Analysis.plot_similarity import plot_similarity
from tscfat.Analysis.cluster_timeseries import cluster_timeseries
from tscfat.Analysis.rolling_statistics import rolling_statistics
from tscfat.Analysis.summary_statistics import summary_statistics

#%%
def process_activity(df,FIGPATH):
    
    #%% filter dataframe and resample hourly means
        
    resampled_interpolated = df.interpolate('linear') 
    timeseries = resampled_interpolated.values
    
    
    # daily / hours for similarity calulation
    resampled_day = resampled_interpolated.resample('D').apply(list)
    data = np.stack(resampled_day.activity.values[1:-1])
    #%%
    _ = summary_statistics(resampled_interpolated.activity,"Time series summary",False,False)
    
    #%% Plot timeseries decompostition and distribution for each component
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Decomposition')
    #FIGPATH = Path(r'F:\tscfat\Results\Decomposition')
    FIGPATH = Path.cwd() / 'Results' /'Decomposition'
    print(FIGPATH)
    FIGNAME = "Battery_level_rolling_statistics" 
    _  = STL_decomposition(timeseries,"Battery level timeseries decomposition", False, FIGPATH,FIGNAME)
       
    #%% rolling stats
    w = 7
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\RollingStatistics')
    #FIGPATH = Path(r'F:\tscfat\Results\RollingStatistics')
    FIGPATH = Path.cwd() / 'Results' /'RollingStatistics'
    FIGNAME = "Battery_level_Rolling_Statistics"
    
    _ = rolling_statistics(resampled_interpolated,w,FIGNAME,FIGPATH)
    
    
    #%% calculate similarity and novelty
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Similarity')
    #FIGPATH = Path(r'F:\tscfat\Results\Similarity')
    FIGPATH = Path.cwd() / 'Results' /'Similarity'
    FIGNAME = "Battery_level_similarity"
    AXIS = resampled_day[1:-1].index.strftime('%m-%d')
    
    sim = calculate_similarity(data,'cosine')
    nov, kernel = compute_novelty(sim,edge=7)
    plot_similarity(sim,nov,"Battery level (cosine distance)",FIGPATH,FIGNAME,(0,0.2),0,AXIS,kernel)

    #%%
    # Timeseries clustering
    #FIGPATH = Path(r'C:\Users\arsii\Documents\Results\Clusters')
    #FIGPATH = Path(r'F:\tscfat\Results\Clusters')
    FIGPATH = Path.cwd() / 'Results' / 'Clusters'
    FIGNAME = "Clustered_timeseries"
    NCLUST  = 3
    clusters = cluster_timeseries(data,FIGNAME, FIGPATH, title="Battery level clustered timeseries", n = NCLUST)
    resampled_fit = resampled_day.iloc[1:-1,:]
    resampled_fit = resampled_fit.assign(clusters = clusters)
    
    #%%
    fig, ax = plt.subplots(NCLUST+1,1,figsize=(6,10))
    fig.suptitle('Daily activity clusters',fontsize=20)
    
    for i in range(NCLUST):
        dfr = resampled_fit[resampled_fit['clusters'] == i]
        mat = dfr.activity.to_numpy()
        mat = np.stack(mat,axis=0)
        mat = np.transpose(mat)
        mea = np.mean(mat,axis=1)
        
        ax[i].plot(mat,':',alpha=0.3)
        ax[i].plot(mea,'b')
        ax[i].set_xlabel('Hour')
        ax[i].set_ylabel('Activity')
        ax[i].set_title('Cluster {}'.format(i))
    
    mat = resampled_fit['activity'].to_numpy()
    #mat = dfr.activity.to_numpy()
    mat = np.stack(mat,axis=0)
    mat = np.transpose(mat)
    mea = np.mean(mat,axis=1)
    
    ax[i+1].plot(mea,'b')
    ax[i+1].set_xlabel('Hour')
    ax[i+1].set_ylabel('Activity')
    ax[i+1].set_title('Average')
    
    fig.tight_layout(pad=1.0)
    plt.show()
        
    #%%
    return df, timeseries, data

if __name__ == "__main__":
    pass
