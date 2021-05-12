#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 23:04:12 2021
@author: arsi
"""

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import MinMaxScaler

from tscfat.Analysis.cluster_timeseries import cluster_timeseries
from tscfat.Utils.doi2int import doi2index

from scipy import stats

from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import mutual_info_score, pairwise_distances

from sl_config_clustering import fn, ap, doi

from datetime import datetime
from matplotlib.dates import date2num

#%%
def calc_MI(x, y, bins=10):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    #mi = mi / np.log(2)
    return mi

#%% load a dataframe and convert the index to datetime
# imputed versions
df_sleep = pd.read_csv('/home/arsii/Data/StudentLife_sleep_i.csv',index_col=0)
df_stress= pd.read_csv('/home/arsii/Data/StudentLife_stress_i.csv',index_col=0)
df_val_aro = pd.read_csv('/home/arsii/Data/StudentLife_valence_arousal_i.csv',index_col=0)
# not imputed
df_activity= pd.read_csv('/home/arsii/Data/Studentlife_activity_data_r.csv',index_col=0)
df_conversation = pd.read_csv('/home/arsii/Data/StudentLife_conversation_r.csv',index_col=0)

#%% combine dataframes
st1 = pd.Timestamp('2013-03-27')
st2 = pd.Timestamp('2013-06-01')
ix = pd.date_range(start=st1, end=st2, freq='D')

# Activity
df_a_c = df_activity.copy(deep=True)
df_a_c.index = pd.to_datetime(df_a_c.index)
df_a_c = df_a_c.groupby('id').resample('H').mean().droplevel(0)
df_a_c['type'] = 'activity'

df_activity.index = pd.to_datetime(df_activity.index)
df_activity = df_activity.groupby('id').resample('D').mean().droplevel(0)
df_activity['type'] = 'activity'

# Conversation
df_c_c = df_conversation.copy(deep=True)
df_c_c.index = pd.to_datetime(df_c_c.index)
df_c_c = df_c_c.groupby('id').resample('H').mean().droplevel(0)
df_c_c['type'] = 'conversation'

df_conversation.index = pd.to_datetime(df_conversation.index)
df_conversation = df_conversation.groupby('id').resample('D').mean().droplevel(0) 
df_conversation['type'] = 'conversation'

df = pd.DataFrame(data = None,
                  index = None,
                  columns = ['id','type','value'])

# Concatenate DataFrames
df = pd.concat([df,df_sleep,df_stress,df_val_aro,df_conversation,df_activity])
df.index = pd.to_datetime(df.index)

# save the dataframe
df.to_csv(r'/home/arsii/Data/StudentLife_cherry_data.csv', header=True)
print(df.isna().sum())
#%% Prepare imputer
imp = IterativeImputer(max_iter=10, random_state=0)
imp.fit([[1, 2], [3, 6], [4, 8], [np.nan, 3], [7, np.nan]])
IterativeImputer(random_state=0)
X_test = [[np.nan, 2], [6, np.nan], [np.nan, 6]]
# the model learns that the second feature is double the first
print(np.round(imp.transform(X_test)))

#%% loop subjects and plot
subjects = [19, 51, 57, 17, 8, 35, 10, 12,  2, 36]

for s in subjects:
    imp = IterativeImputer(max_iter=10, random_state=0)
    df_filt = df[df['id'] == s]
    df_pivot = df_filt.pivot(columns = 'type', values = 'value')
    df_pivot = df_pivot.reindex(ix)

    #df_pivot = df_pivot.interpolate()
    imp.fit(df_pivot.values)
    data = imp.transform(df_pivot.values)
    df_new = pd.DataFrame(data = data,
                          index = df_pivot.index,
                          columns = df_pivot.columns)
    
    df_corr = df_new[['activity','conversation','sleep','stress','valence','arousal']]
    
    X = df_corr.values
    min_max_scaler = MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(X)
    
    test_df = pd.DataFrame(data = x_scaled,    # values
                           index = df_corr.index,   # 1st column as index
                           columns = df_corr.columns)
    

    D = pairwise_distances(test_df.T, Y=None, metric= calc_MI, force_all_finite=True)
    
    axis_labels = ['activity','conversation','sleep','stress','valence','arousal'] # labels for x-axis
    

    # create seabvorn heatmap with required labels
    fig,ax = plt.subplots(1,1,figsize=(15,14))
    sns.heatmap(D, xticklabels = axis_labels, yticklabels = axis_labels, cmap='PuBu_r',annot=True,ax=ax)
    ax.set(title="Subject {} Mutual Information".format(s))
    plt.show()
    
    test_df.rolling(14).mean().plot()
    plt.show()
    
    xcorr = test_df.corr()
    
    fig,ax = plt.subplots(1,1,figsize=(15,14))
    sns.heatmap(xcorr, cmap='RdBu_r',annot=True,ax=ax)
    ax.set(title="Subject {} crosscorrelations".format(s))
    plt.show()

    sns.jointplot(x="arousal", y="valence", data = df_corr, kind="reg")
    
    sns.jointplot(x="activity", y="conversation", data = df_corr, kind="reg")
    
    sns.jointplot(x="valence", y="conversation", data = df_corr, kind="reg")
    
    sns.jointplot(x="sleep", y="stress", data = df_corr, kind="reg")
    #fig,ax = plt.subplots(1,1,figsize=(15,14))
    #sns.pairplot(xcorr)
    #ax.set(title="Subject {} crosscorrelations".format(s))
    #plt.show()
    
#%%

for s in subjects:
    print(df_conversation[df_conversation['id'] == s].shape)
    
#%% PLOT GRUOP AVERAGES

types = ['activity','conversation','sleep','stress','valence','arousal']

for typ in types:
    df_a = df[df['type'] == typ]
    t = df_a.pivot_table(values = 'value', index = df_a.index, columns = ['id'])
    t['median'] = t.median(axis=1)
    t['median'].rolling(14).mean().plot(title = '{} group average'.format(typ))
    plt.show()
    
#%% TEST CLUSTERING ACTIVITY

doi = (2013,4,15),(2013,4,26)
ind_s, ind_e = doi2index(doi,df)

for sub in subjects:
        
        print('Processing ACTIVITY Timeseries Clustering: \n')

        df_sub = df_a_c[df_a_c['id'] == int(sub)]
        
        savename = 'StudentLife_activity_duration_{}.png'.format(sub)
        
        df_daily = df_sub.resample('D').sum()
        df_daily.value.plot(ylabel='Activity duration (h)',title="Daily activity duration \n subject: {}".format(sub),label='Activity')
        df_daily.value.rolling(14).mean().plot(style='k--',label='Rolling Average (14 days)')
        plt.axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")
        plt.legend()
        plt.savefig(savename, format="png")
        
        plt.show()
        
        
        df_sub = df_sub.resample('D').apply(list)
        
    
        data = np.stack(df_sub['2013-03-28':'2013-05-31'].value.values)
        
        clusters = cluster_timeseries(data,
                                      FIGNAME = 'StudentLife_activity_clusters_subject_{}'.format(sub),
                                      FIGPATH = Path('/home/arsii/tscfat/StudentLife/Results/Clustering'),
                                      title = 'Activity {}'.format(sub), 
                                      n = 5, 
                                      metric = 'dtw', 
                                      highlight = (ind_s,ind_e),
                                      ylim_ = None)
        
        cnt = Counter(clusters)
        total = len(clusters)
        weights = [cnt[i] / total for i in clusters]
        df_w = pd.DataFrame(data = weights,
                            index = pd.date_range('2013-03-28', '2013-05-31', freq='D'),
                            columns = ['weight'])
        
        df_w.weight = df_w.weight / df_w.weight.max()
        df_w.rolling(14).mean().plot(title = 'Activity cluster stability / rolling average (14 days) \n Subject: {}'.format(sub),
                                     xlabel = 'Date',
                                     ylabel='Stability', 
                                     ylim = (0.40,1))
        
        savename2 = 'StudentLife_activity_stability_{}.png'.format(sub)
        plt.savefig(savename2, format="png")
        plt.show()
        
print('Done.')

#%% TEST CLUSTERING CONVERSATION
doi = (2013,4,15),(2013,4,26)
ind_s, ind_e = doi2index(doi,df)

index = pd.date_range('2013-03-27', '2013-06-01', freq='H')

for sub in subjects:
        
        print('Processing CONVERSATION Timeseries Clustering: \n')

        df_sub = df_c_c[df_c_c['id'] == int(sub)]
        df_sub = df_sub.reindex(index)
        df_sub.plot()
        plt.show()
        
        savename = 'StudentLife_conversation_duration_{}.png'.format(sub)
        
        df_daily = df_sub.resample('D').sum()
        df_daily.value.plot(ylabel='Conversation duration (min)',xlabel='Date',title="Daily conversation duration \n subject: {}".format(sub))
        df_daily.value.rolling(14).mean().plot(style='k--',label='Rolling Average (14 days)')
        plt.axvspan(date2num(datetime(*doi[0])),date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")
        plt.legend()
        plt.savefig(savename, format="png")
        plt.show()
        
        df_sub = df_sub.resample('D').apply(list)
    
        data = np.stack(df_sub['2013-03-28':'2013-05-31'].value.values)
        
        data[np.isnan(data)] = 0
        
        print(data.shape)
        
        clusters = cluster_timeseries(data,
                                      FIGNAME = 'StudentLife_conversation_clusters_subject_{}'.format(sub),
                                      FIGPATH = Path('/home/arsii/tscfat/StudentLife/Results/Clustering'),
                                      title = 'Conversation {}'.format(sub), 
                                      n = 5, 
                                      metric = 'dtw', 
                                      highlight = (ind_s,ind_e),
                                      ylim_ = None)
        
        cnt = Counter(clusters)
        total = len(clusters)
        weights = [cnt[i] / total for i in clusters]
        df_w = pd.DataFrame(data = weights,
                            index = pd.date_range('2013-03-28', '2013-05-31', freq='D'),
                            columns = ['weight'])
        
        
        df_w.weight = df_w.weight / df_w.weight.max()
        df_w.rolling(14).mean().plot(title = 'Conversation cluster stability / rolling average (14 days) \n Subject: {}'.format(sub),
                                     xlabel = 'Date',
                                     ylabel='Stability', 
                                     ylim = (0.45,0.95))
        
        savename2 = 'StudentLife_conversation_stability_{}.png'.format(sub)
        plt.savefig(savename2, format="png")
        plt.show()
        
print('Done.')

#%% TEST MUTUAL INFORMATION

def calc_MI(x, y, bins=20):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    #mi = mi / np.log(2)
    return mi

X = df_new.values
min_max_scaler = MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(X)
    
test_df = pd.DataFrame(data = x_scaled,    # values
                           index = df_corr.index,   # 1st column as index
                           columns = df_corr.columns)

D = pairwise_distances(X.T, Y=None, metric= calc_MI, force_all_finite=True)
fig,ax = plt.subplots(1,1,figsize=(15,14))
sns.heatmap(D, cmap='RdBu_r',annot=True,ax=ax)
ax.set(title="Subject {} crosscorrelations".format(s))
plt.show()
