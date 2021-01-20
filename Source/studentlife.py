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

#%%
# change correct working directory
WORK_DIR = Path(r'F:\CS-special-assignment')
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

for file in os.listdir(DATA_FOLDER):
    print(file)
    subject = os.path.join(DATA_FOLDER, file)

    df = pd.read_csv(subject)
    
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s',origin='unix')
        df = df.set_index('timestamp')
        df.columns = ['activity']
        df = df[df['activity'] > 0]
        
        resampled = df.resample("H").count()
        
        # create a scaler object
        scaler = MinMaxScaler()
        # fit and transform the data
        df_norm = scaler.fit(resampled['activity'].values.reshape(-1,1))
        resampled['activity'] = df_norm.transform(resampled['activity'].values.reshape(-1,1))
    
    
        FIGPATH = Path(r'F:\CS-special-assignment\Results')
        clusters = process_activity(resampled,FIGPATH)
    except:
        print("Something went horribly wrong!")
#%%
DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Behavior')
subject = DATA_FOLDER / 'Behavior_u00.json'
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
        df_filt = df.filter(["resp_time","level",])
        df_filt = df_filt.set_index('resp_time')
        resampled = df_filt.resample("D").mean()
        resampled.plot()
    except:
        print('Something fishy here')