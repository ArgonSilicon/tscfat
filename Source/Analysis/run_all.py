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

from datetime import datetime
from matplotlib.dates import date2num

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

#%% normalize the dataframe
df2 = df['2020-06-26':'2021-02-09']

from sklearn import preprocessing

X = df2.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(X)

test_df = pd.DataFrame(data = x_scaled,    # values
                       index = df2.index,   # 1st column as index
                       columns = df2.columns)

#%% select columns
cols = ['Sleep Score', 'Average Resting Heart Rate', 'Awake Time',
       'Respiratory Rate', 'Sleep Efficiency', 'Sleep Latency',
       'Total Bedtime', 'Total Sleep Time', 'Average HRV',
       'Lowest Resting Heart Rate', 'Temperature Deviation (°C)',
       'Activity Score', 'Activity Burn', 'Inactive Time', 'Rest Time',
       'Total Burn', 'Non-wear Time', 'Steps', 'Readiness Score', 'active',
       'determined', 'attentive', 'inspired', 'alert', 'afraid', 'nervous',
       'upset', 'hostile', 'ashamed', 'stressed', 'distracted','negative','positive',
       'Communication', 'Entertainment', 'Shop', 'Social_media', 'Sports',
       'Transportation', 'Travel', 'Health', 'Notifications_total',
       'sms_out', 'sms_total', 'sms_in',
       'call_out_duration', 'call_in_duration', 'call_total_duration',
       'call_out_count', 'call_in_count', 'call_total_count',
       'Battery_average','screen_activations', ]

df_sel = test_df[cols]

#%% check some correlations

smooth = df_sel.rolling(window=30).mean()

trend_removed = df_sel - smooth


xcorr = trend_removed['2020-06-26':'2020-09-30'].corr()
fig,ax = plt.subplots(1,1,figsize=(15,14))
sns.heatmap(xcorr, cmap='RdBu_r',annot=False,ax=ax)
plt.title("Cross-correlations '2020-06-26':'2020-09-30'",fontsize=20)

xcorr = trend_removed['2020-10-1':'2020-12-24'].corr()
fig,ax = plt.subplots(1,1,figsize=(15,14))
sns.heatmap(xcorr, cmap='RdBu_r',annot=False,ax=ax)
plt.title("Cross-correlations '2020-10-1':'2020-12-24'",fontsize=20)

xcorr = trend_removed['2020-02-25':'2021-02-9'].corr()
fig,ax = plt.subplots(1,1,figsize=(15,14))
sns.heatmap(xcorr, cmap='RdBu_r',annot=False,ax=ax)
plt.title("Cross-correlations '2020-02-25':'2021-02-9'",fontsize=20)

#%% plot some


for col in cols:
    fig,ax  = plt.subplots(figsize=(15,10))
    test_df[['negative','positive']].rolling(14).mean().plot(style='--', color=['r','g'],ax=ax,ylim=(-0.1,1.1),ylabel='Value',title="Rolling window mean {} : {} : {}".format('negative','positive',col))
    #test_df[col].rolling(14).mean().plot(color='k',ax=ax)
    (bat_re_day['Norm Cluster'].rolling(14).sum() / 14).plot(color='k',ax=ax)
    ax.axvspan(date2num(datetime(2020,10,1)),date2num(datetime(2020,12,24)),ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    plt.show()


#%% SUMMARY STATISTICS
for name in df.columns.to_list():
    
    SAVENAME = name
    SAVEPATH = Path('/home/arsi/Documents/tscfat/Results/Summary')
    ser = df[name]   
    _ = summary_statistics(ser,"{} summary".format(name), savepath = SAVEPATH, savename = SAVENAME, test = False)

#%% STL_DECOMPOSITION
for name in df.columns.to_list(): 
    
    ser = df[name]
    SAVEPATH2 = Path('/home/arsi/Documents/tscfat/Results/Decomposition')
    SAVENAME2 = name + '_decomposition'
    _  = STL_decomposition(ser.values,"{} timeseries decomposition".format(name), False, SAVEPATH2, SAVENAME2, ylabel = 'Value', xlabel = 'Date')
    

#%% ROLLING STATISTICS 
for name in df.columns.to_list():
    
    w = 28
    #ser = df[name].diff(1).diff(7).diff(27).fillna(0)
    ser = df[name]
    FIGPATH = Path('/home/arsi/Documents/tscfat/Results/RollingStatistics')
    FIGNAME = name + '_rolling'
    
    _ = rolling_statistics(ser.to_frame(), w, FIGNAME, FIGPATH)
    
#%% SIMILARITY / NOVELTY / STABILITY
for name in df.columns.to_list():
    
    ser = df[name]
    SAVEPATH3 = Path('/home/arsi/Documents/tscfat/Results/Similarity')
    SAVENAME3 = name + '_similarity'
    AXIS = None
    sim = calculate_similarity(ser.values.reshape(-1,1))
    stab = compute_stability(sim)
    nov, ker = compute_novelty(sim,edge=7)
    plot_similarity(copy.deepcopy(sim),nov,stab,"{} similarity, novelty, and stability".format(name),SAVEPATH3,SAVENAME3,(0,0.06),0.3,AXIS,ker,False)
    

    
#%% CLUSTERING
bat_path = Path('/home/arsi/Documents/Data/Battery.csv')
df_bat = pd.read_csv(bat_path)
df_bat['time'] = pd.to_datetime(df_bat['time'],unit='s')
df_bat = df_bat.set_index(df_bat['time'])
bat_re = df_bat.filter(['battery_level'])
bat_re = bat_re.resample('H').mean()
bat_re = bat_re.interpolate()

bat_re_day = bat_re.resample('D').apply(list)
bat_re_day = bat_re_day['2020-06-26':'2021-02-09']
data = np.stack(bat_re_day.battery_level.values)


FIGPATH = Path.cwd() / 'Results' / 'Clusters'
FIGNAME = "Clustered_timeseries"
# Number of clusters
N = 5 
# max iterations
MI = 5 
# number of iterations for the barycenter
MIB = 5 
# random state
RS = 0
# metric
METRIC = "dtw"  
# highlight
HL = (98,182)
#%% 
clusters = cluster_timeseries(data, FIGNAME, FIGPATH, title="Battery level clustered timeseries", n = N, mi = MI, mib = MIB, rs = RS, metric = METRIC, highlight = HL)


    
