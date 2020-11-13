#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi
"""

# standard library imports
#import os
from pathlib import Path
from datetime import datetime

# change correct working directory
#WORK_DIR = Path('/u/26/ikaheia1/unix/Documents/SpecialAssignment/CS-special-assignment/')
#os.chdir(WORK_DIR)

# third party imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Local application import
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from Plot_similarity import Plot_similarity
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
from save_results import dump_to_json
from plot_timeseries import show_timeseries_scatter, show_timeseries_line, show_features, plot_differences, grouped_histograms
from save2mat import save2mat
from decompose_timeseries import STL_decomposition, detect_steps
from interpolate_missing import interpolate_missing
from cluster_timeseries import cluster_timeseries, gaussian_MM, Agg_Clustering
from tslearn.clustering import TimeSeriesKMeans

    
def process_battery(df,ED,TD,RA,FIGPATH):
    """
    Calculate battery level data analysis, plot and save figures including:
    - battery level distributions by hour
    - Average battery level distribution
    - Battery level difference and pct_change
    - Battery level peaks and bottoms using convolution
    - Battery level STL decomposition
    - Decomposition component histograms
    - Battery level recursion plot and RQA metrics
    - Similarity matric and novelty score
    - Battery level scatterplot
    - Battery level lineplot
    - AIC and BIC score for optimal cluster count evaluation
    - Gaussian Mixture Model clustering
    - TImeseries plotted by clusters
    - Batterety level clusters by day
    - Agglomerative clustering
    
    

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the battery level information
    ED : int
        Embedding dimensions used in RP calculation
    TD : int
        Time delay used in RP calculation
    RA : float
        Neighborhood radius used in RP calculation

    Returns 
    ----------
    df :  pandas dataframe
        Resampled dataframe
    """    
   
   
    #%% filter dataframe and aggregate hourly means
    df_filt = df.filter(["time","battery_level",])
    df_grouped_lists = df_filt.battery_level.groupby(df_filt.index.hour).apply(list) # -> for grouped_histograms()
    resampled = df_filt.resample("H").mean()
    resampled_interpolated, _ = interpolate_missing(resampled,'linear')
    timeseries = resampled_interpolated.values
    
    # daily / hours for similarity calulation
    resampled_day = resampled_interpolated.resample('D').apply(list)
    data = np.stack(resampled_day.battery_level.values[1:-1])
    
    #%% plot histograms
    FIGNAME = "Battery_level" 
    grouped_histograms(df_grouped_lists,'Battery level','Percentage','Proportion',FIGPATH,FIGNAME)
       
    #%% plot differences 
    FIGNAME = "Battery_level"
    lowest, diff, pct = plot_differences(resampled_interpolated, "battery_level","Battery level change in time", "Time (h)", "Difference",FIGPATH,FIGNAME)
    #%% detect steps
    FIGNAME = "Steps"
    peaks, bottoms, top_indices, neg_indices = detect_steps(resampled_interpolated, "Battery level peaks and bottoms", "Time (h)",FIGPATH,FIGNAME)
    #%% Plot timestamps mathing the highest peaks and deepest bottoms:
    # These should indicate timepoints when battery charge rate and drainage is highest.
    high_ts = resampled_interpolated.index[peaks[top_indices]]    
    low_ts = resampled_interpolated.index[bottoms[neg_indices]]
    print("Differencing: ")
    print("Highest battery comsumption:\n",lowest.index)
    print("Gaussian kernel convolution: ")
    print("Highest peaks in battery charge:\n", high_ts)
    print("Highest battery consumption:\n",low_ts)
    #%% Plot timeseries decompostition and distribution for each component
    FIGNAME = "Battery_level_decomposition" 
    _  = STL_decomposition(timeseries,"Battery level timeseries decomposition", FIGPATH,FIGNAME)
        
    #%% calculate recursion plot and metrics
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
        
    #%% show recursion plot and save figure
    FIGNAME = "Battery_level_RP"
    TITLE = "Battery level Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)   
    
    #%% calculate similarity and novelty
    FIGNAME = "Battery_level_similarity"
    AXIS = resampled_day[1:-1].index.strftime('%m-%d')    
    sim = calculate_similarity(data,'cosine')
    nov, kernel = compute_novelty_SSM(sim,L=7)
    Plot_similarity(sim,nov,"Battery level (cosine distance)",False,False,(0,0.04),0.9,AXIS,kernel)
    
    #%% set correct names and save metrics as json 
    RESNAME = "Battery_level_RP_metrics.json"
    dump_to_json(res,FIGPATH,RESNAME)   
    
    # save the timeseries in matlab format
    TSNAME = "Battery_level_ts.mat"
    save2mat(timeseries,FIGPATH,TSNAME)
    
    # save in numpy format
    NPNAME = "Battery_level_ts.npy"
    with open(FIGPATH / NPNAME, mode="wb") as outfile:
        np.save(outfile,timeseries)       
    
    #%% Plot timeseries and save the scatterplot and lineplot
    FIGNAME = "Battery_level_ts_scatter"
    show_timeseries_scatter(resampled_interpolated['battery_level'],"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)
    FIGNAME = "Battery_level_ts_line"
    show_timeseries_line(resampled_interpolated['battery_level'],"Battery level / hourly mean","time","Level",FIGPATH,FIGNAME)
    #%% Extract features from timeseries, plot, and save
    FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Features/')
    FIGNAME = "Battery_level_features"
    show_features(resampled_interpolated['battery_level'],"Battery level ","Time (d)","Value",24,1,"right",False,FIGPATH,FIGNAME)
    
    #%% Clustering
    # resample the dataframe
    df_bl = df['battery_level']
    df_re = df_bl.resample('H').mean()
    df_re, missing = interpolate_missing(df_re,'linear')
    df_grouped = df_re.groupby(df_re.index.floor('d')).apply(list)
    data = np.stack(df_grouped.values[1:-1])
    
    bic = []
    aic = []
    for i in range(2,20):
        model, Y = gaussian_MM(data,i,1000)
        aic.append(model.aic(data))
        bic.append(model.bic(data))
    
    xmin = np.min(bic)
    ix_min = np.argmin(bic)
    ymin = bic[ix_min]
    
    # plot AIC and BIC scores
    fig, ax = plt.subplots(1,2,figsize=(15,7))
    
    ax[0].plot(np.arange(2,20),bic,'o:')
    ax[0].plot(ix_min+2,ymin,'X',c="red",markersize=14)
    ax[0].set_title('BIC score / number of clusters')
    ax[0].set_xlabel('Number of clusters')
    ax[0].set_ylabel('BIC score')
    ax[0].set_xticks(np.arange(2,20))
    
    xmin = np.min(aic)
    ix_min = np.argmin(aic)
    ymin = aic[ix_min]
    
    ax[1].plot(np.arange(2,20),aic,'o:')
    ax[1].plot(ix_min+2,ymin,'X',c="red",markersize=14)
    ax[1].set_title('AIC score / number of clusters')
    ax[1].set_xlabel('Number of clusters')
    ax[1].set_ylabel('AIC score')
    ax[1].set_xticks(np.arange(2,20))
    
    plt.show()
    
    model, Y = cluster_timeseries(df_bl)
    
    #%% agglomerative clustering 
    clust_9, clustering = Agg_Clustering(data,9)
    clust_7, clustering_7 = Agg_Clustering(data,7)
    clust_5, clustering_5 = Agg_Clustering(data,5)
    clust_3, clustering_3 = Agg_Clustering(data,3)
    clust_2, clustering_2 = Agg_Clustering(data,2)
    
    
    print(clustering)
    print(clustering_7)
    print(clustering_5)
    print(clustering_3)
    print(clustering_2)
    
    ##% test tslearn clustering
    km_dtw = TimeSeriesKMeans(n_clusters = 7, metric="dtw", max_iter=5,
                              max_iter_barycenter=5,
                              n_jobs = -1,
                              random_state=0).fit(data)

    
    #%% Assign different clusterings to dataframe
    df_grouped = df_grouped.drop(df_grouped.index[0])
    df_grouped = df_grouped.drop(df_grouped.index[-1])
    clustered_data = df_grouped.to_frame()
    
    clustered_data['cluster_9'] = clustering + 1
    #clustered_data['cluster_7'] = clustering_7 + 1
    clustered_data['cluster_7'] = km_dtw.labels_ +1
    
    clustered_data['cluster_5'] = clustering_5 + 1
    clustered_data['cluster_2'] = clustering_2 + 1
    print("Battery level daily patterns clustered: ")
    print(clustered_data.cluster_7.value_counts())
    
    #%% Plot the clustered timeseries
    battery_mean = data.mean(axis=0)
    val0 = np.stack(clustered_data[clustered_data['cluster_7'] == 1]['battery_level'].values)
    val1 = np.stack(clustered_data[clustered_data['cluster_7'] == 2]['battery_level'].values)
    val2 = np.stack(clustered_data[clustered_data['cluster_7'] == 3]['battery_level'].values)
    val3 = np.stack(clustered_data[clustered_data['cluster_7'] == 4]['battery_level'].values)
    val4 = np.stack(clustered_data[clustered_data['cluster_7'] == 5]['battery_level'].values)
    val5 = np.stack(clustered_data[clustered_data['cluster_7'] == 6]['battery_level'].values)
    val6 = np.stack(clustered_data[clustered_data['cluster_7'] == 7]['battery_level'].values)
    #val7 = np.stack(clustered_data[clustered_data['cluster_9'] == 8]['battery_level'].values)
    #val8 = np.stack(clustered_data[clustered_data['cluster_9'] == 9]['battery_level'].values)
    
    #%%
    fig,ax = plt.subplots(4,2,figsize=(12,15))
    fig.suptitle("Battery level daily development clustered / tslearn cluster averages",fontsize=26,y=1.03)
    
    for i in range(len(val0)):
        ax[0,0].plot(val0[i],':',alpha=0.7)
    ax[0,0].set_title('Clusters: 1',fontsize=22)
    ax[0,0].set_xlabel('Time (hour)',fontsize=18)
    ax[0,0].set_ylabel('Battery level (%)',fontsize=18)
    ax[0,0].set_xlim(-5,105)
    ax[0,0].set_xlim(0,23)
    ax[0,0].plot(val0.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val1)):
        ax[0,1].plot(val1[i],':',alpha=0.7)
    #ax[0,1].patch.set_facecolor('red')
    #ax[0,1].patch.set_alpha(0.15)
    ax[0,1].set_title('Cluster: 2',fontsize=22)
    ax[0,1].set_xlabel('Time (hour)',fontsize=18)
    ax[0,1].set_ylabel('Battery level (%)',fontsize=18)
    ax[0,1].set_xlim(-5,105)
    ax[0,1].set_xlim(0,23)
    ax[0,1].plot(val1.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val2)):
        ax[1,0].plot(val2[i],':',alpha=0.7)
    ax[1,0].set_title('Cluster: 3',fontsize=22)
    ax[1,0].set_xlabel('Time (hour)',fontsize=18)
    ax[1,0].set_ylabel('Battery level (%)',fontsize=18)
    ax[1,0].set_ylim(-5,105)
    ax[1,0].set_xlim(0,23)
    ax[1,0].plot(val2.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val3)):
        ax[1,1].plot(val3[i],':',alpha=0.7)
    ax[1,1].set_title('Cluster: 4',fontsize=22)
    ax[1,1].set_xlabel('Time (hour)',fontsize=18)
    ax[1,1].set_ylabel('Battery level (%)',fontsize=18)
    ax[1,1].set_ylim(-5,105)
    ax[1,1].set_xlim(0,23)
    ax[1,1].plot(val3.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val4)):
        ax[2,0].plot(val4[i],':',alpha=0.7)
    ax[2,0].set_title('Cluster: 5',fontsize=22)
    ax[2,0].set_xlabel('Time (hour)',fontsize=18)
    ax[2,0].set_ylabel('Battery level (%)',fontsize=18)
    ax[2,0].set_ylim(-5,105)
    ax[2,0].set_xlim(0,23)
    ax[2,0].plot(val4.mean(axis=0),c='black')
    #plt.show()
    
    
    for i in range(len(val5)):
        ax[2,1].plot(val5[i],':',alpha=0.7)
    ax[2,1].set_title('Cluster: 6',fontsize=22)
    ax[2,1].set_xlabel('Time (hour)',fontsize=18)
    ax[2,1].set_ylabel('Battery level (%)',fontsize=18)
    ax[2,1].set_ylim(-5,105)
    ax[2,1].set_xlim(0,23)
    ax[2,1].plot(val5.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val6)):
        ax[3,0].plot(val6[i],':',alpha=0.7)
    ax[3,0].set_title('Cluster: 7',fontsize=22)
    ax[3,0].set_xlabel('Time (hour)',fontsize=18)
    ax[3,0].set_ylabel('Battery level (%)',fontsize=18)
    ax[3,0].set_ylim(-5,105)
    ax[3,0].set_xlim(0,23)
    ax[3,0].plot(val6.mean(axis=0),c='black')
    
    ax[3,1].set_title('All Clusters Average',fontsize=22)
    ax[3,1].set_xlabel('Time (hour)',fontsize=18)
    ax[3,1].set_ylabel('Battery level (%)',fontsize=18)
    ax[3,1].set_ylim(-5,105)
    ax[3,1].set_xlim(0,23)
    ax[3,1].plot(battery_mean,c='black')
    
    '''
    for i in range(len(val7)):
        ax[3,1].plot(val7[i],':',alpha=0.7)
    ax[3,1].set_title('Cluster: 8',fontsize=16)
    ax[3,1].set_xlabel('Time (hour)')
    ax[3,1].set_ylabel('Battery level (%)')
    ax[3,1].plot(val7.mean(axis=0),c='black')
    
    for i in range(len(val8)):
        ax[4,0].plot(val8[i],':',alpha=0.7)
    ax[4,0].set_title('Cluster: 9',fontsize=16)
    ax[4,0].set_xlabel('Time (hour)')
    ax[4,0].set_ylabel('Battery level (%)')
    ax[4,0].plot(val8.mean(axis=0),c='black')
    '''
    
    fig.tight_layout(pad=1.0)
    plt.show()
    
    #%% Plot days / clusters
    fig = plt.figure(figsize=(8.3,5))
    ax = fig.add_axes([0,0,1,1])
    clustered_data['cluster_7'].plot(style='o:',label="Clustered Day")
    ax.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of Interest")
    ax.set_title('Battery level daily development clusters',fontsize=22,y=1.02)
    ax.set_ylabel('Cluster no.',fontsize=18)
    ax.set_xlabel('Time (date)',fontsize=18)
    ax.set_ylim(0.5,7.5)
    ax.set_xlim('2020-06-01','2020-08-10')
    ax.legend(fontsize=18)
    plt.show()
    
    #%%
    val0 = np.stack(clustered_data[clustered_data['cluster_2'] == 1]['battery_level'].values)
    val1 = np.stack(clustered_data[clustered_data['cluster_2'] == 2]['battery_level'].values)
    
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,6))
    fig.suptitle("Battery level daily development / cluster averages",fontsize=20,y=1.02)
    
    for i in range(len(val0)):
        ax1.plot(val0[i],':',alpha=0.7)
    ax1.set_title('Clusters: 1',fontsize=16)
    ax1.set_xlabel('Time (hour)')
    ax1.set_ylabel('Battery level (%)')
    ax1.set_xlim(0,100)
    ax1.set_xlim(0,23)
    ax1.plot(val0.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val1)):
        ax2.plot(val1[i],':',alpha=0.7)
    ax2.set_title('Cluster: 2',fontsize=16)
    ax2.set_xlabel('Time (hour)')
    ax2.set_ylabel('Battery level (%)')
    ax2.set_xlim(0,100)
    ax2.set_xlim(0,23)
    ax2.plot(val1.mean(axis=0),c='black')
    
    fig.tight_layout(pad=1.0)
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    clustered_data['cluster_2'].plot(style='o:')
    ax.set_title('Battery level daily development clustered / DTW, 2 clusters')
    ax.set_yticks(np.arange(8))
    ax.set_ylabel('Cluster no.')
    ax.set_xlabel('Time / day')
    ax.set_ylim(0.8,7.2)
    ax.set_xlim('2020-06-01','2020-08-10')
    plt.show()
    
    #%% show some sample days
    g = df.groupby(df.index.floor('d'))
    my_day = pd.Timestamp('2020-07-13')
    my_day_2 = pd.Timestamp('2020-07-14')
    my_day_3 = pd.Timestamp('2020-07-15')
    df_slice = g.get_group(my_day)
    df_slice_2 = g.get_group(my_day_2)
    df_slice_3 = g.get_group(my_day_3)
    #%%
    df_slice.battery_level.plot()
    plt.xlabel("Time / hours")
    plt.ylabel("Battery_level")
    plt.title("Battery level {}".format(my_day.date()))
    plt.ylim(0,105)
    plt.show()
    
    df_slice_2.battery_level.plot()
    plt.xlabel("Time / hours")
    plt.ylabel("Battery_level")
    plt.title("Battery level {}".format(my_day_2.date()))
    plt.ylim(0,105)
    plt.show()
    
    df_slice_3.battery_level.plot()
    plt.xlabel("Time / hours")
    plt.ylabel("Battery_level")
    plt.title("Battery level {}".format(my_day_3.date()))
    plt.ylim(0,105)
    plt.show()
    #%%
    
    df_slice_r = df_slice.resample("H").mean()
    df_slice_r.index = np.arange(24)
    df_slice_r.battery_level.plot.bar(rot=0)
    plt.xlabel("Time / hours")
    plt.ylabel("Battery_level")
    plt.title("Battery level / averages {}".format(my_day.date()))
    plt.ylim(0,105)
    plt.show()
    
    #%%
    df_slice_r2 = df_slice_2.resample("H").mean()
    df_slice_r2.index = np.arange(24)
    df_slice_r2.battery_level.plot.bar(rot=0)
    plt.xlabel("Time / hours")
    plt.ylabel("Battery_level")
    plt.title("Battery level / averages {}".format(my_day_2.date()))
    plt.ylim(0,105)
    plt.show()
    

    #%%
    return df, km_dtw

if __name__ == "__main__":
    pass