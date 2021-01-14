#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is the example script for battery level processing. 
The data is loaded in CSV format. 
The analysis is conducted in process_battery_level.py.

"""
# standard library imports
import os
from pathlib import Path
import re

# change correct working directory
#WORK_DIR = Path(r'C:\Users\arsii\Documents\CS-special-assignment\Source')
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Source')
os.chdir(WORK_DIR)

# third party imports

# Local application imports
from load_csv import load_all_subjects
from process_battery import process_battery


###############################################################################
#%% Load the data into dictionary filenames as keys
#DATA_FOLDER = Path(r'C:\Users\arsii\Documents\CS-special-assignment\Data') # <- REPLACE THIS!
DATA_FOLDER = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Data')
csv_dict = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv_dict.keys()) 

#%% Loop thru keys and assing dataframe if battery data is found
for k in dict_keys:
    if re.search("Battery",k):
        df1 = csv_dict[k]
    else:
        pass

#%% Set parameters and paths 
# path to folder where plot are saved
#FIGPATH = Path(r'C:\Users\arsii\Documents\Results') # <- REPLACE THIS!
FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results')

#%% Process Battery level

_ = process_battery(df1,FIGPATH)

