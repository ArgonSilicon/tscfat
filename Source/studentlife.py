#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:34:34 2021

@author: arsii
"""
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import json
import os

from Source.Analysis.sl_process_activity import process_activity

plt.style.use('seaborn')

def main():
    #%%
    # change correct working directory
    #WORK_DIR = Path(r'F:\tscfat')
    #os.chdir(WORK_DIR)
    
    WORK_DIR = Path(r'/home/arsi/Documents/tscfat')
    #WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat')
    os.chdir(WORK_DIR)
    
    #%%
    '''
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
    '''
    #%%
    #DATA_FOLDER = Path(r'F:\StudentLife\dataset\sensing\activity')
    #DATA_FOLDER = Path.cwd() / 'StudentLife' / 'dataset' / 'sensing' / 'activity'
    DATA_FOLDER = Path(r'/home/arsi/Documents/StudentLife/dataset/sensing/activity')
    first = None
    last = None
    st1 = pd.Timestamp('2013-03-27 04:00:00')
    st2 = pd.Timestamp('2013-06-01 04:00:00')
    ix = pd.date_range(start=st1, end=st2, freq='H')
    mis_mat = np.zeros([1585,49])
    i = 0
    for file in os.listdir(DATA_FOLDER):
        print(file)
        subject = os.path.join(DATA_FOLDER, file)
    
        df = pd.read_csv(subject)
        df.describe()
        
        
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s',origin='unix')
            df = df.set_index('timestamp')
            df.columns = ['activity']
            df[df['activity'] != 0] = 1
                     
            resampled = df.resample('H').sum()
            resampled_counts = df.resample('H').count()
            
            resampled = resampled.reindex(ix)
            resampled_counts = resampled_counts.reindex(ix)
            
            proportions = resampled / resampled_counts
            # STORE THE PROPORTIONS IN A MATRIX AND IMPUTE WITH impute_data.py
          
            interpolated = proportions.interpolate()
            
            missing = proportions.isna().astype(int)
            mis_mat[:,i] = np.transpose(missing.values)
            proportions = proportions.fillna(value=0)
            
            plt.plot(resampled_counts)
            plt.title("Sampling frequency")
            plt.show()
            
            plt.plot(missing)
            plt.title('Missing datapoints')
            plt.show()
            
            m_day = missing.resample("D").sum()
            m_day['time'] = m_day.index
            m_day['time'] = pd.to_datetime(m_day['time'])
            m_day = m_day.groupby(m_day['time'].dt.day_name()).sum()
            m_day.index = pd.Categorical(m_day.index, categories=
                                           ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                           ordered=True)
            m_day = m_day.sort_index()
            m_day.plot(kind='bar',title="Missing datapoints / day",ylabel='Count')
            
            FIGPATH = Path.cwd() / 'Results'
            #print(FIGPATH)
            dp = interpolated.resample("D").mean()
            
            #clusters = process_activity(dp,FIGPATH)
            clusters = process_activity(proportions,FIGPATH)
            i += 1
            
        except:
            print("Something went horribly wrong!")
            i += 1
    
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
     
    ticklabels = [item.strftime('%Y-%m-%d') for item in proportions.index]
    tick_locs = np.linspace(24,len(ticklabels),10)
    
    f1,ax = plt.subplots(figsize=(15,15))
    ax.imshow(np.transpose(mis_mat), aspect='auto',interpolation='none',cmap="Blues")
    ax.set_title('Missing datapoints',fontsize=36)
    ax.set_xlabel('date',fontsize=26)
    ax.set_ylabel('subject',fontsize=26)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=16)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_locator(ticker.FixedLocator(tick_locs))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.show()
               
    #create a pandas dataframe
    subject_list = ["subject_" + str(i+1) for i in range(49)]
    miss_df = pd.DataFrame(data = mis_mat,    
                 index = proportions.index,    
                 columns = subject_list)
    
    m_day = miss_df.resample("D").sum()
    
    day_sums = m_day.sum(axis=1, skipna = True)
    
    day_sums.plot(title='Total daily missing data points')
    
    
    m_day['rowsums'] = m_day.sum(axis = 1, skipna = True)
    
    m_day = m_day.filter(['rowsums'])
    m_day['time'] = m_day.index
    m_day['time'] = pd.to_datetime(m_day['time'])
    
    m_day = m_day.groupby(m_day['time'].dt.day_name()).sum()
    m_day.index = pd.Categorical(m_day.index, categories=
                                           ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                           ordered=True)
    m_day = m_day.sort_index()
    m_day.plot(kind='bar',title="Missing datapoints / day",ylabel='Count')
    
    
    #%%
    '''
    rng=pd.date_range(start=df.index.min(), periods=35, freq='H')
    df.reindex(rng).ffill()
    #%%
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Behavior')
    subject = DATA_FOLDER / 'Behavior_u04.json'
    df = pd.read_json(subject)
    '''
    #%% STRESS
    #DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Stress')
    DATA_FOLDER = Path(r'/home/arsi/Documents/StudentLife/dataset/EMA/response/Stress')
    
    st1 = pd.Timestamp('2013-03-25')
    st2 = pd.Timestamp('2013-06-04')
    ix = pd.date_range(start=st1, end=st2, freq='D')
    
    
    stress_mat = np.empty((72,0), int)
    
    #stress_miss = np.empty((0,70), int)
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_json(current_file)
            df_filt = df.filter(["resp_time","level",])
            df_filt = df_filt.set_index('resp_time')
            
            resampled = df_filt.resample("D").mean()
            resampled = df_filt.reindex(ix)
            
            missing = resampled.level.isna().astype(int)
            missing = missing.values.reshape(1,-1)
            
            stress_mat = np.append(stress_mat, resampled, axis=1)
            
            resampled.plot()
        except:
            print('Something fishy here')
            
    '''      
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
            
    ticklabels = [item.strftime('%Y-%m-%d') for item in resampled.index]
    tick_locs = np.linspace(24,len(ticklabels),10)
    
    f1,ax = plt.subplots(figsize=(15,15))
    ax.imshow(stress_miss, aspect='auto',interpolation='none',cmap="Blues")
    ax.set_title('Missing datapoints',fontsize=36)
    ax.set_xlabel('date',fontsize=26)
    ax.set_ylabel('subject',fontsize=26)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=16)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_locator(ticker.FixedLocator(tick_locs))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.show()
       ''' 
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
    DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\Mood_1')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_json(current_file)
            df_filt = df.filter(["resp_time","tomorrow",])
            df_filt = df_filt.set_index('resp_time')
            resampled = df_filt.resample("D").mean()
            resampled.plot()
        except:
            print('Something fishy here')

    #%%
    #DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\PAM')
    DATA_FOLDER = Path(r'/home/arsi/Documents/StudentLife/dataset/EMA/response/PAM')
    st1 = pd.Timestamp('2013-03-25')
    st2 = pd.Timestamp('2013-06-04')
    ix = pd.date_range(start=st1, end=st2, freq='D')
    
    pam_mat = np.empty((72,0), int)
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_json(current_file)
            df_filt = df.filter(["resp_time","picture_idx",])
            df_filt = df_filt.set_index('resp_time')
            
            
            resampled = df_filt.resample("D").mean()
            resampled = resampled.reindex(ix)
            interpolated = resampled.interpolate()
            
            pam_mat = np.append(pam_mat, interpolated.values, axis=1)
            
            interpolated.plot()
        except:
            print('Something fishy here')
            
    #%%
    #DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\PAM')
    DATA_FOLDER = Path(r'/home/arsi/Documents/StudentLife/dataset/EMA/response/Behavior')
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_json(current_file)
            df_filt = df.filter(["resp_time","anxious",])
            df_filt = df_filt.set_index('resp_time')
            
            resampled = resampled.resample("D").mean()
            resampled = df_filt.reindex(ix)
            resampled.plot()
        except:
            print('Something fishy here')
            
    #%%
    
    # THIS IS SOMETHING THAT NEEDS TO BE DONE WITH EMA SCORES???
    
    # result = df.append([df2])
    # result = result.sort_index()
    # result = (results - result.min()) / (result.max() - result.min()) # column-wise by default
    # result['average'] = result.mean(axis=1)
    # result = result.resample("D").mean()
    # result = result.reindex(ix)
    # result = result.interpolate()
    # fillna?
    
    
    #%%            
if __name__ == '__main__':

    main()