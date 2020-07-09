#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is main file


"""
# standard library imports
import os
from pathlib import Path

# change correct working directory
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

# Local application imports
from csv_load import load_all_subjects
import process_apps, process_ESM, process_battery, process_screen_events, process_location

###############################################################################
#%% Load the data
DATA_FOLDER = Path('/u/26/ikaheia1/data/Documents//SpecialAssignment/Data/CSV/')
csv_dict = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv_dict.keys()) # the order of keys is probably different

###############################################################################
#%% Process Battery level
df1 = csv_dict[dict_keys[4]]
df1_r = process_battery.process_battery(df1)

###############################################################################
#%% Process ESM data
df2 = csv_dict[dict_keys[2]]
df2_r = process_ESM.process_ESM(df2)

##############################################################################
#%% Location / daily
df3 = csv_dict[dict_keys[3]]
df3_r = process_location.process_location(df3)

##############################################################################
#%% Screen events
df4 = csv_dict[dict_keys[0]]
df4_r = process_screen_events.process_screen_events(df4)

###############################################################################
#%% Process App notfications
df = csv_dict[dict_keys[1]]
df_r, ts = process_apps.process_apps(df,df1,df4)


