#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:40:44 2021

@author: arsi
"""

import pandas as pd
	
from tscfat.Analysis.summary_statistics import summary_statistics
	
# load a dataframe and convert the index to datetime
df = pd.read_csv('/home/arsi/Documents/tscfat/Data/one_subject_data.csv',index_col=0)
df.index = pd.to_datetime(df.index)

# Select 'Positive' column and convert it into pandas series
ser = df['positive']

# Rolling window size
w = 14
 
_ = summary_statistics(ser,
                       title = "Time series summary",
                       window = w,
                       savepath = False,
                       savename = False,
                       test = False,
                       )
                       
