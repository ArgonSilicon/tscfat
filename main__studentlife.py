#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

Process the Studentlife conversation data.


"""
# standard library imports
import os
from pathlib import Path
from joblib import Parallel, delayed

# change correct working directory
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

"""
import matplotlib as plt
plt.rcParams.update({'figure.max_open_warning': 0})
"""

# Local application imports
from csv_load import load_all_subjects
from process_conversation import process_conversation
from process_call_logs import process_call_logs
from process_sms import process_sms


if __name__ == "__main__":
    
    #%% Load the conversation data
    DATA_FOLDER = Path('/u/26/ikaheia1/unix/Documents/SpecialAssignment/StudentLife/dataset/sensing/conversation/')
    csv_dict = load_all_subjects(DATA_FOLDER)
    dict_keys = list(csv_dict.keys()) # the order of keys is probably different
    
    #%% Process subjects
    Parallel(n_jobs=4,verbose=1)(delayed(process_conversation)(csv_dict[k], k[-3:]) for k in dict_keys)
    # this yields some nasty error?
    #%% Process without joblib
    for k in dict_keys:
        csv = csv_dict[k]
        key = k[-3:]
        process_conversation(csv,key)
        
   
    #%% load call logs data
    DATA_FOLDER = Path('/u/26/ikaheia1/unix/Documents/SpecialAssignment/StudentLife/dataset/call_log/')
    csv_dict = load_all_subjects(DATA_FOLDER)
    dict_keys = list(csv_dict.keys()) # the order of keys is probably different
    
    # df = csv_dict[dict_keys[15]]
    
    #%% 
    for k in dict_keys:
        df = csv_dict[k]
        key = k[-3:]
        process_call_logs(df,key)
        
    #%% load call logs data
    DATA_FOLDER = Path('/u/26/ikaheia1/unix/Documents/SpecialAssignment/StudentLife/dataset/sms/')
    csv_dict = load_all_subjects(DATA_FOLDER)
    dict_keys = list(csv_dict.keys()) # the order of keys is probably different
    
    # df = csv_dict[dict_keys[15]]
    
    #%% 
    for k in dict_keys:
        df = csv_dict[k]
        key = k[-3:]
        process_sms(df,key)