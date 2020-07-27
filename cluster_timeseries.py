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

def cluster_timeseries(df):
    resampled = df.resample("H").mean()
    resampled_interpolated, _ = interpolate_missing(resampled,'linear')
    
    df_grouped = resampled_interpolated.groupby(resampled_interpolated.index.floor('d')).apply(list)
    data = np.stack(df_grouped.values[1:-1])
    
    # clustering
    for i in range(2,10):
        km = TimeSeriesKMeans(n_clusters = int(i), metric="softdtw", max_iter=50,
                              max_iter_barycenter=50,
                              metric_params={"gamma": .5},
                              random_state=0).fit(data)
    
        labels = km.fit_predict(data)
        sc = silhouette_score(data, labels, metric="softdtw")
        print('No. clusters: {} Silhouette score: {:.4f}'.format(i,sc))
        
    
    km = TimeSeriesKMeans(n_clusters = 5, metric="softdtw", max_iter=50,
                              max_iter_barycenter=50,
                              metric_params={"gamma": .9},
                              random_state=0,
                              n_jobs = -1,
                              verbose = 1).fit(data)
    
    labels = km.fit_predict(data)
    dfp = df_grouped.drop(df_grouped.index[0])
    dfp = dfp.drop(dfp.index[-1])
    clustered_data = dfp.to_frame()
    
    clustered_data['cluster'] = labels + 1
    cntr = Counter(clustered_data['cluster'].values)
    print(cntr.most_common())
    
    
    
    #%% do some plotting
    
    val0 = np.stack(clustered_data[clustered_data['cluster'] == 1]['battery_level'].values)
    val1 = np.stack(clustered_data[clustered_data['cluster'] == 2]['battery_level'].values)
    val2 = np.stack(clustered_data[clustered_data['cluster'] == 3]['battery_level'].values)
    val3 = np.stack(clustered_data[clustered_data['cluster'] == 4]['battery_level'].values)
    val4 = np.stack(clustered_data[clustered_data['cluster'] == 5]['battery_level'].values)
    
    
    
    for i in range(len(val0)):
        plt.plot(val0[i])
        plt.title('Clusters: 1')
    plt.show()
    
    for i in range(len(val1)):
        plt.plot(val1[i])
        plt.title('Cluster: 2')
    plt.show()
    
    for i in range(len(val2)):
        plt.plot(val2[i])
        plt.title('Cluster: 3')
    plt.show()
    
    for i in range(len(val3)):
        plt.plot(val3[i])
        plt.title('Cluster: 4')
    plt.show()
    
    for i in range(len(val4)):
        plt.plot(val4[i])
        plt.title('Cluster: 5')
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    clustered_data['cluster'].plot(style='o:')
    ax.set_title('Battery level daily development clustered')
    ax.set_yticks(np.arange(6))
    ax.set_ylabel('Cluster no.')
    ax.set_xlabel('Time / day')
    ax.set_ylim(0.8,5.2)
    ax.set_xlim('2020-06-01','2020-07-17')
    plt.show()
    
    model, Y =  gaussian_MM(data)
    
    clustered_data['cluster_2'] = Y + 1
    #%% do some plotting
    
    val0 = np.stack(clustered_data[clustered_data['cluster_2'] == 1]['battery_level'].values)
    val1 = np.stack(clustered_data[clustered_data['cluster_2'] == 2]['battery_level'].values)
    val2 = np.stack(clustered_data[clustered_data['cluster_2'] == 3]['battery_level'].values)
    val3 = np.stack(clustered_data[clustered_data['cluster_2'] == 4]['battery_level'].values)
    val4 = np.stack(clustered_data[clustered_data['cluster_2'] == 5]['battery_level'].values)
    
    
    
    for i in range(len(val0)):
        plt.plot(val0[i])
        plt.title('Clusters: 1')
    plt.show()
    
    for i in range(len(val1)):
        plt.plot(val1[i])
        plt.title('Cluster: 2')
    plt.show()
    
    for i in range(len(val2)):
        plt.plot(val2[i])
        plt.title('Cluster: 3')
    plt.show()
    
    for i in range(len(val3)):
        plt.plot(val3[i])
        plt.title('Cluster: 4')
    plt.show()
    
    for i in range(len(val4)):
        plt.plot(val4[i])
        plt.title('Cluster: 5')
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    clustered_data['cluster_2'].plot(style='o:')
    ax.set_title('Battery level daily development clustered')
    ax.set_yticks(np.arange(6))
    ax.set_ylabel('Cluster no.')
    ax.set_xlabel('Time / day')
    ax.set_ylim(0.8,5.2)
    ax.set_xlim('2020-06-01','2020-07-17')
    plt.show()
    
    #%%
    
    return clustered_data,labels, model, Y

def gaussian_MM(data):
    # fit model
    K = 5
    model = GaussianMixture(n_components=K)
    model.fit(data)
    # model properties
    Y = model.predict(data)
    print(Y)
    model_mu = model.means_
    print(model_mu)
    model_cov = model.covariances_
    print(model_cov)
    return model, Y