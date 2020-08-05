#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:07:21 2020

@author: ikaheia1
"""
from collections import Counter
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from interpolate_missing import interpolate_missing
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from calculate_similarity import calculate_distance
from calculate_DTW import DTW_distance

from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
    d_dict = dendrogram(linkage_matrix,truncate_mode='level', p=7)

def cluster_timeseries(df):
    resampled = df.resample("H").mean()
    resampled_interpolated, _ = interpolate_missing(resampled,'linear')
    
    df_grouped = resampled_interpolated.groupby(resampled_interpolated.index.floor('d')).apply(list)
    data = np.stack(df_grouped.values[1:-1])
    
    model, Y =  gaussian_MM(data,7,10000)
    
    df_grouped = df_grouped.drop(df_grouped.index[0])
    df_grouped = df_grouped.drop(df_grouped.index[-1])
    clustered_data = df_grouped.to_frame()
    
    clustered_data['cluster'] = Y + 1
    #%% do some plotting
    
    val0 = np.stack(clustered_data[clustered_data['cluster'] == 1]['battery_level'].values)
    val1 = np.stack(clustered_data[clustered_data['cluster'] == 2]['battery_level'].values)
    val2 = np.stack(clustered_data[clustered_data['cluster'] == 3]['battery_level'].values)
    val3 = np.stack(clustered_data[clustered_data['cluster'] == 4]['battery_level'].values)
    val4 = np.stack(clustered_data[clustered_data['cluster'] == 5]['battery_level'].values)
    val5 = np.stack(clustered_data[clustered_data['cluster'] == 6]['battery_level'].values)
    val6 = np.stack(clustered_data[clustered_data['cluster'] == 7]['battery_level'].values)
    
    fig,ax = plt.subplots(4,2,figsize=(15,15))
    fig.suptitle("Battery level daily development / cluster averages",fontsize=20,y=1.02)
    
    for i in range(len(val0)):
        ax[0,0].plot(val0[i],':',alpha=0.7)
    ax[0,0].set_title('Clusters: 1',fontsize=16)
    ax[0,0].set_xlabel('Time (hour)')
    ax[0,0].set_ylabel('Battery level (%)')
    ax[0,0].set_xlim(0,100)
    ax[0,0].set_xlim(0,23)
    ax[0,0].plot(val0.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val1)):
        ax[0,1].plot(val1[i],':',alpha=0.7)
    ax[0,1].set_title('Cluster: 2',fontsize=16)
    ax[0,1].set_xlabel('Time (hour)')
    ax[0,1].set_ylabel('Battery level (%)')
    ax[0,1].set_xlim(0,100)
    ax[0,1].set_xlim(0,23)
    ax[0,1].plot(val1.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val2)):
        ax[1,0].plot(val2[i],':',alpha=0.7)
    ax[1,0].set_title('Cluster: 3',fontsize=16)
    ax[1,0].set_xlabel('Time (hour)')
    ax[1,0].set_ylabel('Battery level (%)')
    ax[1,0].plot(val2.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val3)):
        ax[1,1].plot(val3[i],':',alpha=0.7)
    ax[1,1].set_title('Cluster: 4',fontsize=16)
    ax[1,1].set_xlabel('Time (hour)')
    ax[1,1].set_ylabel('Battery level (%)')
    ax[1,1].plot(val3.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val4)):
        ax[2,0].plot(val4[i],':',alpha=0.7)
    ax[2,0].set_title('Cluster: 5',fontsize=16)
    ax[2,0].set_xlabel('Time (hour)')
    ax[2,0].set_ylabel('Battery level (%)')
    ax[2,0].plot(val4.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val5)):
        ax[2,1].plot(val5[i],':',alpha=0.7)
    ax[2,1].set_title('Cluster: 6',fontsize=16)
    ax[2,1].set_xlabel('Time (hour)')
    ax[2,1].set_ylabel('Battery level (%)')
    ax[2,1].plot(val5.mean(axis=0),c='black')
    #plt.show()
    
    for i in range(len(val6)):
        ax[3,0].plot(val6[i],':',alpha=0.7)
    ax[3,0].set_title('Cluster: 7',fontsize=16)
    ax[3,0].set_xlabel('Time (hour)')
    ax[3,0].set_ylabel('Battery level (%)')
    ax[3,0].plot(val6.mean(axis=0),c='black')
    
    fig.tight_layout(pad=1.0)
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    clustered_data['cluster'].plot(style='o:')
    ax.set_title('Battery level daily development clustered')
    ax.set_yticks(np.arange(8))
    ax.set_ylabel('Cluster no.')
    ax.set_xlabel('Time / day')
    ax.set_ylim(0.8,7.2)
    ax.set_xlim('2020-06-01','2020-07-17')
    plt.show()
       
    return model, Y

def gaussian_MM(data,K=5,n=10):
    
    # fit model
    model = GaussianMixture(n_components=K,n_init=n,covariance_type="full")
    model.fit(data)
    # model properties
    Y = model.predict(data)
    print(Y)
    model_mu = model.means_
    print(model_mu)
    model_cov = model.covariances_
    print(model_cov)
    return model, Y

def Agg_Clustering(timeseries,n_clusters=7):
    metric = DTW_distance
    dist = calculate_distance(timeseries,metric)
    #dist = calculate_distance(timeseries,"cosine")

    clustering = AgglomerativeClustering(n_clusters,
                                         affinity='precomputed',
                                         memory=None,
                                         connectivity=None,
                                         compute_full_tree='auto',
                                         linkage='complete',
                                         distance_threshold=None).fit(dist)
    
    """
    model = AgglomerativeClustering(distance_threshold=0,affinity="precomputed",linkage='complete', n_clusters=None)
    model = model.fit(dist)
    fig = plt.figure(figsize=(10,10))
    
    plt.title('Hierarchical Clustering Dendrogram')
    # plot the top three levels of the dendrogram
    plot_dendrogram(clustering, truncate_mode='level', p=7)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.xticks(rotate=45)
    plt.show()
    """
    
    return clustering.labels_    


