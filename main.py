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
import re

# change correct working directory
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

# Local application imports
from csv_load import load_all_subjects
import process_apps, process_ESM, process_battery, process_screen_events, process_location

###############################################################################
#%% Load the data
DATA_FOLDER = Path('/u/26/ikaheia1/data/Documents''/SpecialAssignment/Data/CSV/')
csv_dict = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv_dict.keys()) # the order of keys is probably different

#%% loop thru keys and assing dataframes
for k in dict_keys:
    if re.search("Battery",k):
        df1 = csv_dict[k]
        
    elif re.search("ESM",k):
        df2 = csv_dict[k]
        
    elif re.search("Location",k):
        df3 = csv_dict[k]
        
    elif re.search("Screen",k):
        df4 = csv_dict[k]
        
    elif re.search("Application",k):
        df5 = csv_dict[k]
        
    else:
        raise Exception("Dictionary key unknown.") 
###############################################################################
#%% Process Battery level
df1_r = process_battery.process_battery(df1)

###############################################################################
#%% Process ESM data
df2_r, ts_2 = process_ESM.process_ESM(df2)

##############################################################################
#%% Location / daily
df3_r = process_location.process_location(df3)

##############################################################################
#%% Screen events
df4_r = process_screen_events.process_screen_events(df4)

###############################################################################
#%% Process App notfications
df5_r, ts_5 = process_apps.process_apps(df5,df1,df4)

#%%
df5_a = df5_r[df5_r['is_active'] == True]

df5_f = df5_a.filter(['Communication', 'Entertainment', 'Other', 'Shop', 'Social_media',
       'Sports', 'Travel', 'Work/Study'])

df5_d = df5_f.resample('D').sum()

#%% combine dataframes

comb = pd.concat([df2_r,df5_d], axis=1)

#%%
def corrfunc(x,y, ax=None, **kws):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, _ = spearmanr(x, y)
    ax = ax or plt.gca()
    # Unicode for lowercase rho (ρ)
    rho = '\u03C1'
    ax.annotate(f'{rho} = {r:.2f}', xy=(.1, .9), xycoords=ax.transAxes)
    
g = sns.pairplot(comb,kind="reg")
g.map_lower(corrfunc)
g.fig.suptitle("ESM data pairplots and Spearman correlation", y=1.02,fontsize=20)

#%%
corr_p = comb.corr(method ='pearson') 
corr_s = comb.corr(method ='spearman')
corr_k = comb.corr(method ='kendall')