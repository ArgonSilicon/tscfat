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
import seaborn as sns
import re

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from StudentLife.process_activity_sl import process_activity
from binned_conversation import calculate_binned_conversation
from PAM_encoder import PAM_encoder


plt.style.use('seaborn')

def main():
    #%%
    # change correct working directory
    #WORK_DIR = Path(r'F:\tscfat')
    #os.chdir(WORK_DIR)
    
    WORK_DIR = Path(r'/home/arsii/tscfat')
    #WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat')
    os.chdir(WORK_DIR)
    
    #%%
    df_path = Path('/home/arsii/Data/Studentlife_cherry_data.csv')
    df = pd.read_csv(df_path, index_col=0,parse_dates=True)
    
    #%%
    dtypes = {
        "id" : "category",
        "type": "category",
        "value": "float64" ,
        }
    sl = pd.DataFrame(data=None, index= None, columns = ['id','type','value'])#,dtype = dtypes)
    
    cherry = ['51','02','12','10','57','35','19','36','17','08']

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
    activity_miss_dict = {}
    i = 0
    for file in os.listdir(DATA_FOLDER):
        print(file)
        subject = os.path.join(DATA_FOLDER, file)
        res = re.findall("u(\d+).csv", file)
    
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
            
            if res[0] in cherry:
                interpolated['id'] = res[0]
                interpolated['type'] = 'activity'
                interpolated = interpolated.rename(columns={'activity':'value'})
                sl = pd.concat([sl,interpolated])
                
            missing = proportions.isna().astype(int)
            
            activity_miss_dict[res[0]] = missing.values.flatten().sum()
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
    
    
    
    activity_miss_dict = dict(sorted(activity_miss_dict.items(), key=lambda item: item[1]))
    
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
    
    sl.to_csv(r'/home/arsi/Documents/Data/Studentlife_cherry_data.csv', header=True)
    
    #df.to_csv(r'/home/arsii/Data/Studentlife_cherry_data.csv', header=True)
    



    


    #%% Converstion duration
    DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/sensing/conversation')
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        res = re.findall("u(\d+).csv", current_file)
        
        if res[0] in cherry:
            print(res[0])
           
            try:
                df_c = pd.read_csv(current_file)
                df_c.columns = ['start_timestamp','end_timestamp'] 
                df_c['start_timestamp'] = pd.to_datetime(df_c['start_timestamp'],unit='s',origin='unix')
                df_c['end_timestamp'] = pd.to_datetime(df_c['end_timestamp'],unit='s',origin='unix')
                ts,tr = calculate_binned_conversation(df_c)
                
                duration_df = pd.DataFrame(data = ts,    # values
                                           index = tr,   # 1st column as index
                                           columns = ['value'])
                
                duration_df['id'] = int(res[0])
                duration_df['type'] = 'conversation'
                
                df = pd.concat([df,duration_df])
                
            except:
                print('fail')            

    #%% plot conversationo durations
    
    for c in cherry:
        df[(df['id'] == int(c)) & (df['type'] == 'conversation')].plot()
        
    for c in cherry:
        df[(df['id'] == int(c)) & (df['type'] == 'activity')].value.rolling(14).mean().plot()
        plt.show()
        
    for c in cherry:
        df[(df['id'] == int(c)) & (df['type'] == 'conversation')].value.rolling(14).mean().plot()
        plt.show()

    for c in cherry:
        df[(df['id'] == int(c)) & (df['type'] == 'sleep')].value.rolling(14).mean().plot()
        plt.show()
        
    
        
    #%% save the new dataframe
    #df.to_csv(r'/home/arsii/Data/Studentlife_cherry_data.csv', header=True)
    #%%re
    #DATA_FOLDER = Path(r'F:\StudentLife\dataset\EMA\response\PAM')
    DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/EMA/response/PAM')
    st1 = pd.Timestamp('2013-03-27')
    st2 = pd.Timestamp('2013-06-01')
    ix = pd.date_range(start=st1, end=st2, freq='D')
    
    pam_mat = np.empty((67,0), int)
    pam_miss_dict = {}
    
    df_empty = pd.DataFrame(data = None,
                            index = None,
                            columns = ['id','type','value'])
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        res = re.findall("u(\d+).json", current_file)
        
        if res[0] in cherry:
            try:
                df = pd.read_json(current_file)
                df_filt = df.filter(["resp_time","picture_idx",])
                df_filt = df_filt.set_index('resp_time')
                
                valence = []
                arousal = []
                
                for i in df_filt.values: 
                    v,a = PAM_encoder(i)
                    valence.append(v)
                    arousal.append(a)
                
                df_filt['valence'] = valence
                df_filt['arousal'] = arousal
                 
                
                resampled = df_filt.resample("D").mean()
                re_ix = resampled.reindex(ix)
                interpolated = re_ix.interpolate()
                
                val = interpolated.valence.to_frame()
                val.columns = ['value']
                val['id'] = int(res[0])
                val['type'] = 'valence'
                
                aro = interpolated.arousal.to_frame()
                aro.columns = ['value']
                aro['id'] = int(res[0])
                aro['type'] = 'arousal'
                
                df_empty = pd.concat([df_empty,val])
                df_empty = pd.concat([df_empty,aro])
                """
                missing = re_ix.picture_idx.isna().astype(int)
                missing = missing.values.reshape(-1,1)
                miss_sum = missing.flatten().sum()
                pam_miss_dict[res[0]] = miss_sum
                
                pam_mat = np.append(pam_mat, missing, axis=1)
                
                re_ix.plot()
                
                resampled_day = df_filt.resample('H').mean()
                
                
                if res[0] in cherry:
                    resampled_day['id'] = res[0]
                    resampled_day['type'] = 'PAM'
                    resampled_day = resampled_day.rename(columns={'picture_idx':'value'})
                    sl = pd.concat([sl,resampled_day])
                """
            except:
                print('Something fishy here')
            
        '''
        df = pd.read_json(current_file)
        df_filt = df.filter(["resp_time","picture_idx",])
        df_filt = df_filt.set_index('resp_time')
        
        
        resampled = df_filt.resample("D").mean()
        re_ix = resampled.reindex(ix)
        #interpolated = resampled.interpolate()
        
        missing = re_ix.picture_idx.isna().astype(int)
        missing = missing.values.reshape(-1,1)
        
        pam_mat = np.append(pam_mat, missing, axis=1)
        
        re_ix.plot()
        
    pam_miss_dict = dict(sorted(pam_miss_dict.items(), key=lambda item: item[1]))
    plt.imshow(np.transpose(pam_mat))
    plt.title('PAM / missing data')
    plt.ylabel("Subject no.")
    plt.xlabel("Time(day)")
    plt.show()
    
    fig = plt.figure(figsize=(10,2))
    plt.scatter(np.arange(72),pam_mat[:,0])
    plt.title('Worst case')
    plt.ylabel('Missingness')
    plt.xlabel('Time(day)')
    plt.show()
    
    fig = plt.figure(figsize=(10,2))
    plt.scatter(np.arange(72),pam_mat[:,1])
    plt.title('Best case')
    plt.ylabel('Missingness')
    plt.xlabel('Time(day)')
    plt.show()
    
    fig = plt.figure(figsize=(10,2))
    plt.scatter(np.arange(72),pam_mat[:,7])
    plt.title('Typical case')
    plt.ylabel('Missingness')
    plt.xlabel('Time(day)')
    plt.show()
    
    #sl.to_csv(r'/home/arsi/Documents/Data/Studentlife_cherry_data.csv', header=True)
         '''
    df_empty.to_csv(r'/home/arsii/Data/valence_arousal.csv', header=True)
    
    for c in cherry:
        df_empty[(df_empty['id'] == int(c)) & (df_empty['type'] == 'arousal')].value.rolling(14).mean().plot(title = 'Arousal: {}'.format(c))
        plt.show()
        
    for c in cherry:
        df_empty[(df_empty['id'] == int(c)) & (df_empty['type'] == 'valence')].value.rolling(14).mean().plot(title = 'Valence: {}'.format(c))
        plt.show()
            
    #%%
    ids = df.id.unique()
    
    df_act = df[(df['id'] == i) & (df['type'] == 'activity') ].value.resample('D').sum()
    df_act = df_act.reindex(ix)
    df_act.plot()
    
    #%% Sleep
    DATA_FOLDER = Path('/home/arsii/StudentLife/dataset/EMA/response/Sleep')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        res = re.findall("u(\d+).json", current_file)
        
        if res[0] in cherry:
            print(res[0])
           
            try:
                df_s = pd.read_json(current_file)

                df_s['resp_time'] = pd.to_datetime(df_s['resp_time'],unit='s',origin='unix')
                df_s = df_s.set_index('resp_time')
                df_s.sort_index()
                
                df_s = df_s.resample('D').mean()
                df_s = df_s.reindex(ix)
                df_s = df_s.interpolate()
                
    
                
                sleep_df = pd.DataFrame(data = df_s.hour.values,    # values
                                        index = df_s.index,   # 1st column as index
                                        columns = ['value'])
                
                sleep_df['id'] = int(res[0])
                sleep_df['type'] = 'sleep'
                
                df = pd.concat([df,sleep_df])
                
            except:
                print('fail')
    
    #%% Sleep
    DATA_FOLDER = Path('/home/arsii/StudentLife/dataset/EMA/response/Stress')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        res = re.findall("u(\d+).json", current_file)
        
        if res[0] in cherry:
            print(res[0])
           
            try:
                df_s = pd.read_json(current_file)

                df_s['resp_time'] = pd.to_datetime(df_s['resp_time'],unit='s',origin='unix')
                df_s = df_s.set_index('resp_time')
                df_s.sort_index()
                
                df_s = df_s.resample('D').mean()
                df_s = df_s.reindex(ix)
                df_s = df_s.interpolate()
                
    
                
                stress_df = pd.DataFrame(data = df_s.level.values,    # values
                                        index = df_s.index,   # 1st column as index
                                        columns = ['value'])
                
                stress_df['id'] = int(res[0])
                stress_df['type'] = 'stress'
                
                df = pd.concat([df,stress_df])
                
            except:
                print('fail')
    #%% Conversation duration
    
    DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/sensing/conversation')
    
    for file in os.listdir(DATA_FOLDER):
        print(file)
        current_file = os.path.join(DATA_FOLDER, file)
        res = re.findall("u(\d+).csv", current_file)
        
        if res[0] in cherry:
            print(res[0])
           
            try:
                df_c = pd.read_csv(current_file)
                df_c.columns = ['start_timestamp','end_timestamp'] 
                df_c['start_timestamp'] = pd.to_datetime(df_c['start_timestamp'],unit='s',origin='unix')
                df_c['end_timestamp'] = pd.to_datetime(df_c['end_timestamp'],unit='s',origin='unix')
                ts,tr = calculate_binned_conversation(df_c)
                
                duration_df = pd.DataFrame(data = ts,    # values
                                           index = tr,   # 1st column as index
                                           columns = ['value'])
                
                duration_df['id'] = int(res[0])
                duration_df['type'] = 'conversation'
                
                df = pd.concat([df,duration_df])
                
            except:
                print('fail')
    #%%
    from sklearn import preprocessing
    
    
    for i in cherry:
        print(i)
        df_pam = df[(df['id'] == int(i)) & (df['type'] == 'PAM')].value.resample('D').median()
        df_pam = df_pam.interpolate()
        df_pam = df_pam.reindex(ix)
        df_pam = df_pam.to_frame()
        
        val = []
        aro = []
        
        for v in df_pam.value.values:
            if not np.isnan(v):
                va,ar = PAM_encoder(v)
                val.append(va)
                aro.append(ar)
            else:
                val.append(np.nan)
                aro.append(np.nan)
                
        df_pam['valence'] = val
        df_pam['arousal'] = aro

        df_act = df[(df['id'] == int(i)) & (df['type'] == 'activity') ].value.resample('D').sum()
        df_act = df_act.interpolate()
        df_act = df_act.reindex(ix)
        df_act = df_act.to_frame()
        df_act = df_act.rename(columns={'value':'activity'})
        
        df_conv = df[(df['id'] == int(i)) & (df['type'] == 'conversation') ].value.resample('D').sum()
        df_conv = df_conv.interpolate()
        df_conv = df_conv.reindex(ix)
        df_conv = df_conv.to_frame()
        df_conv = df_conv.rename(columns={'value':'conversation'})
        
        df_sleep = df[(df['id'] == int(i)) & (df['type'] == 'sleep') ].value.resample('D').mean()
        df_sleep = df_sleep.interpolate()
        df_sleep = df_sleep.reindex(ix)
        df_sleep = df_sleep.to_frame()
        df_sleep = df_sleep.rename(columns={'value':'sleep'})
        
        df_stress = df[(df['id'] == int(i)) & (df['type'] == 'stress') ].value.resample('D').mean()
        df_stress = df_stress.interpolate()
        df_stress = df_stress.reindex(ix)
        df_stress = df_stress.to_frame()
        df_stress = df_stress.rename(columns={'value':'stress'})
        
        comb_df = pd.concat([df_pam['valence'],df_pam['arousal'],df_act['activity'],df_conv['conversation'],df_sleep['sleep'],df_stress['stress']], axis=1)
        
        
        
        X = comb_df.values
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(X)

        test_df = pd.DataFrame(data = x_scaled,    # values
                               index = comb_df.index,   # 1st column as index
                               columns = comb_df.columns)
        
        print('eek')
    
        #fig = plt.figure(figsize=(10,10))
        #df_pam.rolling(14).valence.mean().plot(label='Valence')
        #df_pam.rolling(14).arousal.mean().plot(label='Arousal')
        #df_act.rolling(14).mean().plot(label='Activity')
        test_df.rolling(14).mean().plot(title='Subject: {}'.format(i),ylim=(-0.1,1.1))
        #plt.show()
        xcorr = test_df.corr()
        fig,ax = plt.subplots(1,1,figsize=(15,14))
        sns.heatmap(xcorr, cmap='RdBu_r',annot=True,ax=ax)
        ax.set(title="Subject {} crosscorrelations".format(i))
        
     
    #%%
     
    for i in ids:
        df[(df['id'] == i) & (df['type'] == 'activity') ].resample('D').sum().value.plot(ylim=(0,13),title='subject: {}'.format(i))
        plt.show()
    
    
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

    for i in cherry:
        print(i)
        df[(df['id'] == str(i)) & (df['type'] == 'conversation')].resample('D').sum().rolling(14).mean().plot()
    
    
    #%%
    
    df_cut = df.loc['2013-03-27':'2013-06-01']
   
    
   
    #%% check some group level means
    
    st1 = pd.Timestamp('2013-03-27')
    st2 = pd.Timestamp('2013-06-01')
    ix = pd.date_range(start=st1, end=st2, freq='D')
    
    # activity
    df_a = df_cut[df_cut['type'] == 'activity']
    df_p = df_cut[df_cut['type'] == 'PAM']
    df_c = df_cut[df_cut['type'] == 'conversation']
    df_sl = df_cut[df_cut['type'] == 'sleep']
    df_st = df_cut[df_cut['type'] == 'stress']
      
    #df_a = df_a.resample('D').mean()
    
    df_test = df_p
    
    arr = np.zeros((10,67))
    
    for i,j in enumerate(cherry, start=0):
        df_loop = df_test[df_test['id'] == int(j)]
        
        df_loop = df_loop.resample('D').median()
    
        df_loop = df_loop.reindex(ix)
        df_loop = df_loop.interpolate()
        df_loop = df_loop.fillna(value = df_loop.value.mean(skipna=True))#, method = 'bfill')
        
        arr[i,:] = df_loop.value.values
        plt.plot(df_loop.value.values)
        plt.show()
    
    summary_df = pd.DataFrame(data = np.transpose(arr),    # values
                               index = ix)  # 1st column as index
                              
    summary_df.mean(axis=1).plot(title='PAM Group average',ylabel='Level')
    plt.show()
    
if __name__ == '__main__':

    main()
