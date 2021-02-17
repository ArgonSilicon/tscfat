#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 09:53:21 2021

@author: arsi
"""

import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import json
import os
import seaborn as sns
import scipy.stats as stats
import itertools

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

WORK_DIR = Path(r'/home/arsi/Documents/tscfat')
#WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat')
os.chdir(WORK_DIR)

from Source.Analysis.sl_process_activity import process_activity
from Source.Analysis.assign_labels import assign_groups
from Source.Analysis.vector_encoding import decode_string, decode_string_3

plt.style.use('seaborn')

def crosscorr(datax, datay, lag=0, wrap=False):
        """ Lag-N cross correlation. 
        Shifted data filled with NaNs 
        
        Parameters
        ----------
        lag : int, default 0
        datax, datay : pandas.Series objects of equal length
    
        Returns
        ----------
        crosscorr : float
        """
        if wrap:
            shiftedy = datay.shift(lag)
            shiftedy.iloc[:lag] = datay.iloc[-lag:].values
            return datax.corr(shiftedy,method='pearson')
        
        else: 
            return datax.corr(datay.shift(lag),method='pearson')

#%%
GROUP_LABEL_CSV_PATH = Path('/home/arsi/Documents/Data/esm_groups.csv/')
esm_path = Path('/home/arsi/Documents/Data/ESM.csv')
df = pd.read_csv(esm_path)
df = assign_groups(df,GROUP_LABEL_CSV_PATH)

df['time'] = pd.to_datetime(df['time'],unit='s')
df = df.set_index(df['time'])

#%% Check NaN's
#df_nans = df.groupby[]
df.isna().sum().plot(kind='bar')  
plt.show()
print(df.isna().any())
# df.dropna() / df.fillna(0)

#%%

mask1 = df["type"] == 1
mask2 = df["type"] == 2
mask3 = df["type"] == 3
mask6 = df["type"] == 6
df['scaled_answer'] = 0

# fill nan's
df.loc[mask6,'scaled_answer'] = df.loc[mask6,'answer'].fillna(np.round((df.loc[mask6,'answer'].astype(float).mean())))
df.loc[mask3,"answer"] = df.loc[mask3,"answer"].fillna('empty')

df.loc[mask1,"scaled_answer"] = df.loc[mask1,"answer"].map(decode_string)
df.loc[mask2,"scaled_answer"] = df.loc[mask2,"answer"].map(decode_string)
df.loc[mask3,"scaled_answer"] = df.loc[mask3,"answer"].map(decode_string_3)

sequence = zip(df['scaled_answer'].values,df['negate_value'].values)
x = lambda i : 0 if i == 1 else 1
df['scaled_answer'] = [x(i) if neg == True else i for i,neg in sequence]

#df.loc[mask1,"Scaled_answer"] = df.loc[mask1,"answer"] 
#df.loc[mask2,"Scaled_answer"] = df.loc[mask2,"answer"] 
#df.loc[mask3,"Scaled_answer"] = normalize_values(df.loc[mask3,"answer"].values.astype(float))
#df.loc[mask6,"Scaled_answer"] = normalize_values(df.loc[mask6,"answer"].values.astype(float))

#%%
#df_filt = df.filter(["time","Scaled_answer",])
df_filt = df.filter(["time","group","negate_value","scaled_answer",])
#df_filt = df_filt["Scaled_answer"].astype(int)
df_filt['scaled_answer'] = df_filt["scaled_answer"].astype(int)
#resampled = df_filt.resample("D").apply(custom_resampler)

#%% Positive and negative affects

# Positive
df_temp = df[df['title'] == 'Right now I feel Active']
df_temp = df_temp['scaled_answer'].astype('int64')
active = df_temp.resample('D').mean()

df_temp = df[df['title'] == 'Right now I feel Determined']
df_temp = df_temp['scaled_answer'].astype('int64')
determined = df_temp.resample('D').mean()

df_temp = df[df['title'] == 'Right now I feel Attentive']
df_temp = df_temp['scaled_answer'].astype('int64')
attentive = df_temp.resample('D').mean()

df_temp = df[df['title'] == 'Right now I feel Inspired']
df_temp = df_temp['scaled_answer'].astype('int64')
inspired = df_temp.resample('D').mean()

df_temp = df[df['title'] == 'Right now I feel Alert']
df_temp = df_temp['scaled_answer'].astype('int64')
alert = df_temp.resample('D').mean()

# Negative
df_temp2 = df[df['title'] == 'Right now I feel Afraid']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
afraid = df_temp2.resample('D').mean()

df_temp2 = df[df['title'] == 'Right now I feel Nervous']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
nervous = df_temp2.resample('D').mean()

df_temp2 = df[df['title'] == 'Right now I feel Upset']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
upset = df_temp2.resample('D').mean()

df_temp2 = df[df['title'] == 'Right now I feel Hostile']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
hostile = df_temp2.resample('D').mean()

df_temp2 = df[df['title'] == 'Right now I feel Ashamed']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
ashamed = df_temp2.resample('D').mean()

df_temp2 = df[df['title'] == 'Right now I feel Stressed']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
stressed = df_temp2.resample('D').mean()
stressed_max = df_temp2.resample('D').max()

df_temp2 = df[df['title'] == 'Right now I feel Distracted']
df_temp2 = df_temp2['scaled_answer'].astype('int64')
distracted = df_temp2.resample('D').mean()
#%%


#%%
def main():
    #%%
    # change correct working directory
    #WORK_DIR = Path(r'F:\tscfat')
    #os.chdir(WORK_DIR)
    
    WORK_DIR = Path(r'/home/arsi/Documents/tscfat')
    #WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat')
    os.chdir(WORK_DIR)
    
    #%%
    st1 = pd.Timestamp('2020-06-26')
    st2 = pd.Timestamp('2021-02-10')
    ix = pd.date_range(start=st1, end=st2, freq='D')
    #%%
    affections = pd.concat([active,determined,attentive,inspired,alert,afraid,nervous,upset,hostile,ashamed,stressed,distracted],axis=1)
    affections.columns=['active','determined','attentive','inspired','alert','afraid','nervous','upset','hostile',
                              'ashamed','stressed','distracted']
    #%%
    DATA_FOLDER = Path(r'/home/arsi/Documents/Data/oura_2020-06-26_2021-02-10_trends.csv')
    
    df = pd.read_csv(DATA_FOLDER)
    df.describe()
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    df = df.asfreq(freq="D")
    
    #X = np.array([[1, 2], [3, 6], [4, 8], [np.nan, 3], [7, np.nan]])
    
    X = df.to_numpy()
    
    imp = IterativeImputer(max_iter=10, random_state=0)

    imp.fit(X)

    #IterativeImputer(random_state=0)

    #X_test = [[np.nan, 2], [6, np.nan], [np.nan, 6]]

    # the model learns that the second feature is double the first
    #print(np.round(imp.transform(X_test)))
    
    X_imp = imp.transform(X)
    
    df_imp = pd.DataFrame(data = X_imp,    # values
                          index = df.index,   # 1st column as index
                          columns = df.columns)  # 1st row as the column names

    aff_re = affections.reindex(df_imp.index)
    
    #df_imp.index = pd.to_datetime(df_imp.index)
    
    result = pd.concat([df_imp, aff_re], axis=1)
    
    combinations = list(itertools.combinations(result.columns.to_list(), 2))
  
    # cross correlation
    xcorr = result.corr()
    
    sns.heatmap(xcorr, annot=False)

    #xmat = xcorr.to_numpy()
    #%%
    
    
    #%%
    for pair in combinations: 
        #%%
        overall_pearson_r = result[pair[0]].corr(result[pair[1]])#.corr().iloc[0,17]
        #print(f"Pandas computed Pearson r: {overall_pearson_r}")
        
        if (0.2 < abs(overall_pearson_r) < 0.5):
            print(pair)
            r, p = stats.pearsonr(result.dropna()[pair[0]], result.dropna()[pair[1]])
            #print(f"Scipy computed Pearson r: {r} and p-value: {p}")
            
            df_filt = result.filter([pair[0],pair[1],])
            
            scaler = MinMaxScaler()
            scaler.fit(df_filt)
            #print(scaler.data_max_)
            scaled = scaler.transform(df_filt)
            
            df_scaled = pd.DataFrame(data = scaled,    # values
                                     index = df_filt.index,    # 1st column as index
                                     columns = [pair[0],pair[1],]) # 1st row as the column names
            '''
            fig,ax = plt.subplots(figsize=(14,3))
            df_scaled.rolling(window=7,center=True).mean().plot(ax = ax)
            ax.set(xlabel='Frame',ylabel='Normalized Value')
            ax.set(title=f"Rolling window mean score / Overall Pearson r = {np.round(overall_pearson_r,2)}");
            plt.show()
            '''
            #%%
            # Set window size to compute moving window synchrony.
            r_window_size = 7
             
            # Compute rolling window synchrony
            rolling_r = df_scaled[pair[0]].rolling(window = r_window_size, center = True).corr(df_scaled[pair[1]])
            
            # plot
            f,ax = plt.subplots(2,1,figsize = (14,6),sharex = True)
            df_scaled.rolling(window = r_window_size, center = True).mean().plot(ax = ax[0])
            ax[0].set(xlabel = 'Date',ylabel = 'Normalized value')
            rolling_r.plot(ax = ax[1])
            ax[1].set(xlabel = 'Date',ylabel = 'Pearson r')
            plt.suptitle("Rolling window (size = {}) mean and correlation \n Overal pearson correlation: {}".format(r_window_size, np.round(overall_pearson_r,2)))
            plt.show()    
            #%%
            
        
            d1 = df_scaled[pair[0]]
            d2 = df_scaled[pair[1]]
            r_window_size = 14
            rs = [crosscorr(d1,d2, lag) for lag in range(-int(r_window_size),int(r_window_size+1))]
            offset = -(np.floor(len(rs)/2) - np.argmax(rs))
            
            f,ax=plt.subplots(figsize=(14,3))
            ax.plot(np.arange(-14,15,1),rs)
            ax.axvline(np.ceil(len(rs)/2) - (r_window_size + 1), color = 'k',linestyle = ':', label = 'Center')
            ax.axvline(np.argmax([abs(x) for x in rs]) - r_window_size, color = 'r', linestyle = '--', label = 'Peak synchrony',alpha = 0.5)
            ax.set(title=f'Offset = {offset} days\n  {pair[0]} leads <> {pair[1]} leads')
            ax.set(ylim = [-1,1], xlim = [-14,14],)
            ax.set(xlabel = 'Offset (days)', ylabel = 'Pearson r')
            ax.set_xticklabels([int(item) for item in ax.get_xticks()]);
            plt.legend()
            plt.show()
            
            #%%
            # Windowed time lagged cross correlation
            window = 14
            max_lag = 7
            no_splits = 15
            samples_per_split = int(df_scaled.shape[0] / no_splits)
            rss = []
            
            for t in range(0, no_splits-1):
                d1 = df_scaled[pair[0]][(t) * window : (t+2) * window]
                d2 = df_scaled[pair[1]][(t) * window : (t+2) * window]
                rs = [crosscorr(d1, d2, lag) for lag in range(-int(max_lag), int(max_lag+1))]
                rss.append(rs)
            
            rss = pd.DataFrame(rss)
            
            f,ax = plt.subplots(figsize=(10,10))
            sns.heatmap(rss,cmap='RdBu_r',ax=ax, annot=True,fmt='.1f')
            ax.set(title=f'Windowed Time Lagged Cross Correlation \n {pair[0]} leads <> {pair[1]} leads')
            ax.set(xlim=[0,15])
            ax.set(xlabel='Offset',ylabel='Window epochs')
            ax.set_xticklabels(np.arange(-7,8,1))#[int(item-7) for item in ax.get_xticks()]);
            plt.show()
        
        #%%
        # Rolling window time lagged cross correlation
        '''
        window = 7
        window_size = 15 #samples
        t_start = 0
        t_end = t_start + window_size
        step_size = 15
        rss=[]
        
        while t_end < 225:
            d1 = df_scaled[pair[0]].iloc[t_start:t_end]
            d2 = df_scaled[pair[1]].iloc[t_start:t_end]
            rs = [crosscorr(d1,d2, lag, wrap = False) for lag in range(-int(window),int(window + 1))]
            rss.append(rs)
            t_start = t_start + step_size
            t_end = t_end + step_size
        rss = pd.DataFrame(rss)
        
        f,ax = plt.subplots(figsize=(10,10))
        sns.heatmap(rss,cmap='RdBu_r',ax=ax)
        ax.set(title=f'Rolling Windowed Time Lagged Cross Correlation',xlim=[0,15], xlabel='Offset',ylabel='Epochs')
        ax.set_xticklabels(np.arange(-7,8,1))#[int(item) for item in ax.get_xticks()]);
        
        
        '''
        
#%%
from calculate_similarity import calculate_similarity




#%%
if __name__ == "__main__":
    main()