# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 11:18:24 2021

@author: arsii
"""

import numpy as np
import pandas as pd
from pathlib import Path


class ArgLoader(object):
    def setup_np():
        
        open_name =  Path(r'F:\CS-special-assignment\Data\Battery_test_data_1.csv')
        #open_name = Path('/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Data/Battery_test_data_1.csv')
        with open_name.open('r') as read_file:
            df = pd.read_csv(read_file)
            df['time'] = pd.to_datetime(df['time'],unit = 's')
            return df['battery_level'].values
        
    
    def setup_ps():
    
        open_name =  Path(r'F:\CS-special-assignment\Data\Battery_test_data_1.csv')
        #open_name = Path('/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Data/Battery_test_data_1.csv')
        with open_name.open('r') as read_file:
            df = pd.read_csv(read_file)
            df['time'] = pd.to_datetime(df['time'],unit = 's')
            return df['battery_level']
        
    def setup_pd():
        
        open_name =  Path(r'F:\CS-special-assignment\Data\Battery_test_data_1.csv')
        #open_name =  Path(r'C:\Users\arsii\Documents\CS-special-assignment\Data\Battery_test_data_1.csv')
        #open_name = Path('/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Data/Battery_test_data_1.csv')
        with open_name.open('r') as read_file:
            df = pd.read_csv(read_file)
            df['time'] = pd.to_datetime(df['time'],unit = 's')
            return df