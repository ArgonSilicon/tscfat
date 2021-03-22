#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is the example script for battery level processing. 
The data is loaded in CSV format. 
The analysis is conducted in process_battery_level.py.
The results are stored on disk.

"""
import pandas as pd

from Source.Analysis.config import fn, ap, doi

from Source.Analysis.summary_statistics import summary_statistics
from Source.Analysis.rolling_statistics import rolling_statistics


#%%
print(fn.csv_path)
print(fn.list_filenames())

#%% LOAD THE DATA FRAME
df = pd.read_csv(fn.csv_path)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])
df = df.drop(columns=['date','Other','Work/Study'])

#%% SUMMARY STATISTICS
print('Processing Summary Statistics: ')
i = 1
for name in df.columns.to_list():        
    print('Column: {:30s} : {}/{}'.format(name,i,df.shape[1]))
    i += 1
    ser = df[name] 
    sn = fn.summary_base + '_' + name
    _ = summary_statistics(ser,
                           "{} summary".format(name),
                           ap.summary_window,
                           fn.summary_out,
                           sn,
                           False)
    

#%% ROLLING STATISTICS 
print("Processing Rolling Statistics: ")
i = 1
for name in df.columns.to_list():
    print('Column: {:30s} : {}/{}'.format(name,i,df.shape[1]))
    i += 1
    ser = df[name] 
    savename = fn.rolling_base + '_' + name
    _ = rolling_statistics(ser.to_frame(),
                           ap.rolling_window,
                           doi = doi,
                           savename = savename,
                           savepath = fn.rolling_out,
                           test = False)
    
#%%

'''
def main():
    # change correct working directory
    #WORK_DIR = Path(r'F:\tscfat') # <- WINDOWS
    WORK_DIR = Path('/u/26/ikaheia1/data/Documents/tscfat')
    #WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat')
    os.chdir(WORK_DIR)
    
    # third party imports
    
    # Local application imports
    from Source.Utils.load_csv import load_all_subjects
    from Source.Analysis.process_battery import process_battery
    
    
    ###############################################################################
    #%% Load the data into dictionary filenames as keys
    #DATA_FOLDER = Path(r'F:\tscfat\Data') # <- WINDOWS
    #DATA_FOLDER = Path(r'/mnt/f/tscfat/Data')
    DATA_FOLDER = Path.cwd() / 'Data' 
    DATA_FOLDER = Path('/home/arsi/Documents/Data/')
    #DATA_FOLDER = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/tscfat/Data')
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
    #FIGPATH = Path(r'F:\tscfat\Results') # <- WINDOWS
    #FIGPATH = Path(r'/mnt/f/tscfat/Results')
    FIGPATH = Path.cwd() / 'Results'
    #FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results')
    
    #%% Process Battery level
    
    _ = process_battery(df1,FIGPATH)

if __name__ == '__main__':

    main()
'''