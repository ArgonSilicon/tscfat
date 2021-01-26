#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:34:34 2021

@author: arsii
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import json
import os

from Source.Analysis.sl_process_activity import process_activity

def main():
    #%%
    # change correct working directory
    WORK_DIR = Path(r'F:\tscfat')
    os.chdir(WORK_DIR)
    
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA')
    subject = DATA_FOLDER / 'EMA_definition.json'
    df = pd.read_json(subject)
    
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\survey')
    subject = DATA_FOLDER / 'panas.csv'
    df = pd.read_csv(subject)
    
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\sensing\phonecharge')
    subject = DATA_FOLDER / 'phonecharge_u00.csv'
    df = pd.read_csv(subject)
    
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\sensing\activity')
    
    first = None
    last = None
    st1 = pd.Timestamp('2013-03-27 04:00:00')
    st2 = pd.Timestamp('2013-06-01 04:00:00')
    ix = pd.date_range(start=st1, end=st2, freq='H')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        subject = os.path.join(DATA_FOLDER, file)
    
        df = pd.read_csv(subject)
        
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s',origin='unix')
            df = df.set_index('timestamp')
            df.columns = ['activity']
            
            '''
            start = df.index[0]
            end = df.index[-1]
            
            if not first:
                first = start
            if not last:
                last = end
            if end > last:
                last == end
            if start < first:
                first = start
            '''
            
            df_active = df[df['activity'] > 0] # subject is active
            resampled_active = df_active.resample("H").count()
            resampled_active = resampled_active.reindex(ix)
            
            # fo missing data
            resampled = df.resample("H").sum(min_count=1)
            resampled = resampled.reindex(ix) 
            
            missing_values = resampled.isna().astype(int)
            missing_values.plot(title="Missing datapoints / hourly")
            print(missing_values.shape)
            
            m_day = missing_values.resample("D").sum()
            m_day['time'] = m_day.index
            m_day['time'] = pd.to_datetime(m_day['time'])
            m_day = m_day.groupby(m_day['time'].dt.day_name()).sum()
            m_day.index = pd.Categorical(m_day.index, categories=
                                           ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                           ordered=True)
            m_day = m_day.sort_index()
            m_day.plot(kind='bar',title="Missing datapoints",ylabel='Count')
            
            # create a scaler object
            scaler = MinMaxScaler()
            # fit and transform the data
            df_norm = scaler.fit(resampled_active['activity'].values.reshape(-1,1))
            resampled['activity'] = df_norm.transform(resampled['activity'].values.reshape(-1,1))
        
        
            FIGPATH = Path(r'F:\tscfat\Results')
            clusters = process_activity(resampled,FIGPATH)
        except:
            print("Something went horribly wrong!")
            
    #%%
    rng=pd.date_range(start=df.index.min(), periods=35, freq='H')
    df.reindex(rng).ffill()
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Behavior')
    subject = DATA_FOLDER / 'Behavior_u04.json'
    df = pd.read_json(subject)
    
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Stress')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_json(current_file)
            df_filt = df.filter(["resp_time","level",])
            df_filt = df_filt.set_index('resp_time')
            resampled = df_filt.resample("D").mean()
            resampled.plot()
        except:
            print('Something fishy here')
        
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Mood')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_json(current_file)
            df_filt = df.filter(["resp_time","happy",])
            df_filt = df_filt.set_index('resp_time')
            resampled = df_filt.resample("D").mean()
            resampled.plot()
        except:
            print('Something fishy here')

    #%%            
if __name__ == '__main__':

    main()