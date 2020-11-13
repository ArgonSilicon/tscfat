#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:22:44 2020

@author: ikaheia1

Calculate hourly binned statistics for events having starting and 
ending times.

"""
import pandas as pd
import numpy as np
#from time import process_time 


def calculate_binned_conversation(df):
    """
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    timesum : TYPE
        DESCRIPTION.
    tr : TYPE
        DESCRIPTION.

    """
    # TODO: fix docstrings and write assertions
    
    first_ts = df['start_timestamp'][0]
    last_ts = df['end_timestamp'][df.shape[0]-1] + pd.Timedelta(hours=1)
       
    #%%
    tr =  pd.date_range(pd.Timestamp(first_ts.strftime('%Y-%m-%d-%H')),pd.Timestamp(last_ts.strftime('%Y-%m-%d-%H')),freq='H')
    df_s = df['start_timestamp'].values
    df_e = df['end_timestamp'].values
    df_s_ts = [pd.Timestamp(i) for i in df_s]
    df_e_ts = [pd.Timestamp(i) for i in df_e]
    st_h = [pd.Timestamp((j.strftime('%Y-%m-%d-%H'))) for j in df_s_ts]
    
    #%%
    t0 = 0
    #t1_start = process_time()
    
    timesum = np.zeros(tr.shape[0])
    
    
    for i in range(tr.shape[0]-1):
        ts = tr[i] # timestamp iterated
        ts_stop = tr[i+1]
        
        for j in range(t0,df.shape[0]):
            
            # TODO: fix this, works really slow!
            start_hour = st_h[j] #pd.Timestamp((df_s_ts[j].strftime('%Y-%m-%d-%H')))
            
            
            if ts < start_hour:
                break
            
            if ts == start_hour: # found matching date + hour
                k = i # helper variable
                start = df_s_ts[j]
                end = df_e_ts[j]
                
                while end > ts_stop: # check if conv ends after ts_stop
                    timesum[k] +=  (ts_stop - start).total_seconds() # add to current timesum: timestamp stop - start
                    k += 1 # increase k by one -> next timestamp
                    start = ts_stop # update start to be the end of current timestamp stop
                    ts_stop = tr[k] # update ts_stop to next timestamp
                   
                timesum[k] += (end - start).total_seconds()
                t0 += 1
  
    return timesum, tr