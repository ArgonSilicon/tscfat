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
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

# third party imports

# Local application imports
from csv_load import load_all_subjects
from process_battery_level import process_battery


###############################################################################
#%% Load the data into dictionary filenames as keys
DATA_FOLDER = Path('/u/26/ikaheia1/data/Documents''/SpecialAssignment/Data/CSV/') # <- REPLACE THIS!
csv_dict = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv_dict.keys()) 

#%% Loop thru keys and assing dataframe if battery data is found
for k in dict_keys:
    if re.search("Battery",k):
        df1 = csv_dict[k]
    else:
        pass

#%% Set parameters and paths 

# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.5 # neigborhood radius
# path to folder where plot are saved
FIGPATH = Path(r'/u/26/ikaheia1/unix/Documents/SpecialAssignment/Results/Figures/') # <- REPLACE THIS!

#%% Process Battery level
df1_r, km_dtw = process_battery(df1,ED,TD,RA,FIGPATH)
