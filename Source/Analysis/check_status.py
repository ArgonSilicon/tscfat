#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:36:43 2020

@author: arsi
"""
import pandas as pd

def check_screen_status(screen_df,target):
    
    assert isinstance(target, pd._libs.tslibs.timestamps.Timestamp), "Given target \"{}\" is not a pandas Timestamp.".format(target)
    assert isinstance(screen_df, pd.core.frame.DataFrame), "Given dataframe is not a pandas dataframe."
    
    
    if 'screen_status' in screen_df.columns:
         status = screen_df.truncate(after=target).iloc[-1]['screen_status']
         if status == 3:
             return True
         else:
             return False
    else:
        raise Exception('There is no column named \"screen_status\" in the dataframe.')

def check_battery_status(battery_df, target):
    
    assert isinstance(target, pd._libs.tslibs.timestamps.Timestamp), "Given target \"{}\" is not a pandas Timestamp.".format(target)
    assert isinstance(battery_df, pd.core.frame.DataFrame), "Given dataframe is not a pandas dataframe."
    
    if 'battery_level' in battery_df.columns:
         status = battery_df.truncate(after=target).iloc[-1]['battery_level']
         if status != 0:
             return True
         else:
             return False
    else:
        raise Exception('There is no column named \"battery_level\" in the dataframe.')
        
