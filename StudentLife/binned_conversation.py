#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:39:38 2021

@author: arsi

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
    
    df['duration'] = (df['end_timestamp'] - df['start_timestamp']).dt.total_seconds()
    
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
    
    t = 0
    bs = tr[t]
    be = tr[t+1]
    # array to store the durations
    timesum = np.zeros(tr.shape[0])
    
    for i in range(len(df_s_ts)):
        
        # iterate conversation start and end
        ts = df_s_ts[i]
        te = df_e_ts[i]
        
        # adjust then bin start and end
        while ts > be:
            t += 1
            bs = tr[t]
            be = tr[t+1]
        
        while(True):
            if te < be:
                timesum[t] += (te-ts).total_seconds()
                break
            
            else:
                timesum[t] += (be-ts).total_seconds()
                ts = be
                t += 1
                bs = tr[t]
                be = tr[t+1]
    
    
    return timesum, tr